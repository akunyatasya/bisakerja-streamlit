# Data Leakage Report - BisaKerja Notebooks

Tanggal audit: 2026-06-01

## Ringkasan Eksekutif

Audit dilakukan pada notebook di folder `notebooks/`:

1. `notebooks/data_wrangling.ipynb`
2. `notebooks/eda_analysis.ipynb`

Kesimpulan utama:

- Tidak ditemukan training model supervised, train-test split, scaler, encoder, atau evaluasi model formal di kedua notebook. Jadi, belum ada data leakage langsung pada metrik model karena metrik model memang belum dibuat.
- Namun, ada beberapa risiko leakage yang penting jika output notebook ini dipakai untuk modeling, terutama pada dataset resume dan dataset training-ready.
- Risiko paling besar ada pada kolom `Required_Skills` di `techtalent_profile_cleaned.csv`, karena nilainya deterministik terhadap `Job_Role`. Jika kolom ini dipakai sebagai fitur untuk memprediksi `Job_Role`, model akan belajar jawaban target secara tidak langsung.
- File `indotech_job_train.csv` bukan train split independen, melainkan hampir sama dengan `indotech_job_cleaned.csv` dan hanya difilter dengan `is_train_ready`.

## Status Leakage Saat Ini

| Area | Status | Catatan |
|---|---|---|
| EDA deskriptif | Aman bersyarat | Analisis memakai seluruh data, tetapi masih wajar untuk eksplorasi deskriptif. |
| Evaluasi model | Belum ada | Tidak ada train-test split atau metrik model yang dapat dinilai leakage-nya. |
| Dataset resume untuk klasifikasi role | Risiko tinggi | `Required_Skills` satu-ke-satu dengan `Job_Role`. |
| Dataset job training | Risiko sedang | `indotech_job_train.csv` adalah subset quality gate, bukan split train/eval. |
| Fitur pipeline/debug | Risiko sedang | Kolom label/audit dapat membocorkan keputusan pipeline jika dipakai sebagai fitur model. |

## Temuan Detail

### 1. Target Leakage pada `Required_Skills` terhadap `Job_Role`

Lokasi:

- `data_wrangling.ipynb`, cell 60-64
- `eda_analysis.ipynb`, cell 3 dan 22

Notebook membersihkan dan mempertahankan kolom `Required_Skills`, lalu EDA membuat `required_skill_list`, `required_skill_count`, dan `skill_gap_count`.

Bukti dari data processed:

| Job_Role | Jumlah variasi `Required_Skills` |
|---|---:|
| Backend Developer | 1 |
| Business Analyst | 1 |
| Cloud Engineer | 1 |
| Cybersecurity Analyst | 1 |
| Data Scientist | 1 |
| ML Engineer | 1 |
| Web Developer | 1 |

Artinya, setiap role hanya memiliki satu template `Required_Skills`. Jika model klasifikasi `Job_Role` menggunakan `Required_Skills`, `required_skill_list`, `required_skill_count`, atau fitur turunan dari kolom tersebut, model dapat menebak target dari pola requirement, bukan dari kemampuan kandidat yang benar-benar independen.

Severity: tinggi untuk use case klasifikasi `Job_Role`.

Rekomendasi:

- Untuk model yang memprediksi `Job_Role`, jangan gunakan `Required_Skills` atau fitur turunannya sebagai input.
- Gunakan fitur kandidat yang tersedia sebelum target diketahui, misalnya `Skills`, `Projects`, `Education`, dan `Experience`.
- Jika `Required_Skills` tetap dipakai, posisikan sebagai referensi eksternal untuk skill gap analysis setelah role/job target sudah ditentukan, bukan sebagai fitur prediksi role.

### 2. `indotech_job_train.csv` Bukan Train Split Independen

Lokasi:

- `data_wrangling.ipynb`, cell 58 dan 71

Notebook membuat `is_train_ready` berdasarkan quality gate:

- `fit_input_quality_score >= 60`
- `skills_count_total >= 1`
- `description_length_chars >= 100`

Lalu menyimpan:

- `indotech_job_cleaned.csv`: 1,679 baris
- `indotech_job_train.csv`: 1,678 baris

Bukti dari data processed:

- Semua baris di `indotech_job_train.csv` memiliki `is_train_ready = 1`.
- `indotech_job_train.csv` overlap 1,678 dari 1,678 `job_id` dengan `indotech_job_cleaned.csv`.
- Jadi file train hanya menghapus 1 baris dari cleaned dataset.

Severity: sedang.

Risiko:

- Nama file `train` dapat menimbulkan salah interpretasi seolah-olah dataset ini sudah aman untuk evaluasi model.
- Jika model dilatih dan dievaluasi kembali pada `indotech_job_cleaned.csv`, hampir seluruh data evaluasi sudah pernah muncul di training.

Rekomendasi:

- Ubah pemaknaan `indotech_job_train.csv` menjadi "modeling-ready dataset", bukan train split.
- Buat split eksplisit, misalnya `train`, `validation`, dan `test`, berbasis `job_id`.
- Untuk data lowongan kerja, pertimbangkan time-based split berdasarkan `source_posted_at` agar evaluasi lebih menyerupai skenario produksi.

### 3. Baseline dan Threshold EDA Dibangun dari Seluruh Dataset

Lokasi:

- `eda_analysis.ipynb`, cell 5, 9, 13, 17, 22, 45

Contoh:

- `top10_skills` dihitung dari seluruh `jobs`.
- `entry_skill_set` dan `entry_required_set` dihitung dari seluruh lowongan entry-level.
- `role_mapped`, distribusi role, korelasi, normality test, ANOVA, dan Kruskal-Wallis memakai seluruh `jobs_eda`.

Untuk EDA, ini masih wajar karena tujuannya membaca kondisi dataset. Namun, jika hasil ini dipakai sebagai baseline model, threshold produksi, atau pembanding evaluasi tanpa holdout, maka informasi dari data evaluasi sudah ikut membentuk aturan analisis.

Severity: sedang untuk modeling, rendah untuk EDA murni.

Rekomendasi:

- Pisahkan mode EDA dan mode modeling.
- Untuk modeling, hitung baseline skill, role mapping hasil tuning, threshold overlap, imputer, dan statistik lain hanya dari training set.
- Terapkan artifact yang sudah dipelajari dari train ke validation/test tanpa menghitung ulang dari seluruh data.

### 4. Kolom Pipeline dan Debug Berpotensi Membocorkan Label

Lokasi:

- `data_wrangling.ipynb`, cell 46, 58, 71
- `eda_analysis.ipynb`, cell 3

Kolom yang perlu diwaspadai:

- `_is_tech_cat`
- `_is_tech_title`
- `_is_tech_skills`
- `is_tech`
- `tech_signal_source`
- `is_train_ready`
- `fit_input_quality_score`
- `fit_input_has_requirements`
- `fit_input_has_skills`

Kolom tersebut berguna untuk audit pipeline, tetapi tidak selalu aman sebagai fitur model. Misalnya, jika target model adalah klasifikasi tech/non-tech, kolom `is_tech` jelas merupakan label. Jika target adalah kualitas input atau readiness, `is_train_ready` dan quality flags dapat menjadi bocoran langsung.

Severity: sedang.

Rekomendasi:

- Simpan kolom audit di dataset audit, tetapi drop dari feature matrix saat modeling.
- Buat daftar eksplisit `FEATURE_COLUMNS` dan `EXCLUDE_COLUMNS`.
- Validasi pipeline training agar kolom target, label, dan audit tidak masuk ke model secara tidak sengaja.

### 5. Imputasi Global pada `source_posted_at`

Lokasi:

- `data_wrangling.ipynb`, cell 54

Notebook mengisi missing `source_posted_at` menggunakan median dari seluruh dataset tech setelah filtering.

Untuk EDA, dampaknya kecil. Untuk modeling, ini termasuk risiko leakage ringan jika fitur tanggal dipakai dalam model, karena median dihitung menggunakan data yang seharusnya berada di validation/test.

Severity: rendah sampai sedang, tergantung apakah fitur tanggal dipakai untuk model.

Rekomendasi:

- Dalam pipeline modeling, fit imputer hanya pada train set.
- Simpan nilai median dari train, lalu gunakan nilai yang sama untuk validation/test.
- Untuk time-based evaluation, pertimbangkan tidak mengimputasi tanggal dengan statistik masa depan.

### 6. Filtering Resume Menggunakan `Job_Role`

Lokasi:

- `data_wrangling.ipynb`, cell 60

Notebook menghapus role non-tech berdasarkan `Job_Role`: `Doctor`, `Mechanical Engineer`, dan `Embedded Engineer`.

Ini bukan leakage jika tujuan dataset memang hanya membangun populasi kandidat tech. Namun, ini menjadi leakage/selection bias jika model nantinya diklaim mampu membedakan kandidat tech vs non-tech, karena kelas non-tech sudah dibuang berdasarkan label.

Severity: rendah untuk tech-only analysis, sedang untuk classifier umum.

Rekomendasi:

- Dokumentasikan bahwa dataset resume final hanya untuk domain tech.
- Jika ingin model dapat menolak non-tech candidate, simpan dataset non-tech sebagai holdout atau kelas negatif.

## Hal yang Tidak Dianggap Leakage

Beberapa langkah berikut tidak termasuk leakage dalam konteks saat ini:

- Strip HTML pada `description` dan `requirement_summary`, karena transformasinya row-wise.
- Normalisasi separator skill, karena tidak memakai target global.
- Mapping `Education` ke format Indonesia, karena transformasinya deterministik.
- Analisis Q1-Q4 sebagai EDA, selama tidak diklaim sebagai evaluasi model prediktif.
- Penggunaan taxonomy eksternal, selama taxonomy dikunci sebelum evaluasi dan tidak dituning menggunakan hasil test.

## Rekomendasi Implementasi Aman untuk Modeling

### Split Data

Gunakan split eksplisit sebelum training:

```python
from sklearn.model_selection import train_test_split

train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    stratify=df["target_column"],
)

valid_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42,
    stratify=temp_df["target_column"],
)
```

Untuk lowongan kerja, split berbasis waktu lebih disarankan jika `source_posted_at` cukup lengkap:

```python
df = df.sort_values("source_posted_at")
train_df = df.iloc[: int(len(df) * 0.70)]
valid_df = df.iloc[int(len(df) * 0.70): int(len(df) * 0.85)]
test_df = df.iloc[int(len(df) * 0.85):]
```

### Kolom yang Sebaiknya Dikeluarkan dari Fitur Model

Untuk model `Job_Role`:

```python
EXCLUDE_COLUMNS = [
    "ID",
    "Job_Role",
    "Required_Skills",
    "required_skill_list",
    "required_skill_count",
    "skill_gap_count",
]
```

Untuk model job matching atau tech classification:

```python
EXCLUDE_COLUMNS = [
    "job_id",
    "is_tech",
    "tech_signal_source",
    "_is_tech_cat",
    "_is_tech_title",
    "_is_tech_skills",
    "is_train_ready",
    "fit_input_quality_score",
    "fit_input_has_requirements",
    "fit_input_has_skills",
]
```

### Prinsip Pipeline

1. Split data terlebih dahulu.
2. Fit preprocessing hanya pada train.
3. Transform validation/test memakai artifact dari train.
4. Jangan gunakan target, label pipeline, atau fitur turunan target sebagai input.
5. Simpan EDA artifact dan modeling artifact secara terpisah.

## Kesimpulan

Notebook saat ini aman untuk EDA deskriptif, tetapi belum aman jika langsung dipakai sebagai dasar evaluasi model. Perbaikan paling penting adalah:

1. Jangan gunakan `Required_Skills` untuk memprediksi `Job_Role`.
2. Jangan menganggap `indotech_job_train.csv` sebagai train split final.
3. Buat split train/validation/test yang eksplisit.
4. Drop kolom audit/label pipeline sebelum modeling.
5. Fit statistik preprocessing hanya pada training set.

Dengan perubahan tersebut, risiko data leakage dapat ditekan sebelum proyek masuk ke tahap modeling dan evaluasi performa.
