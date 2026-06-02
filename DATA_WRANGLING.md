# Data Wrangling Report

Dokumen ini menjelaskan proses data wrangling secara formal untuk proyek BisaKerja, mencakup temuan kualitas data, tindakan pembersihan, serta alasan perubahan ukuran dataset dari raw ke processed.

---

## 1. Ringkasan Eksekutif

### Ukuran data sebelum dan sesudah wrangling
- Raw job dataset: 3,883 baris x 126 kolom
- Processed tech job dataset: 1,679 baris x 34 kolom
- Processed training-ready dataset: 1,678 baris x 34 kolom
- Processed non-tech dataset: 1,395 baris x 31 kolom
- Raw resume dataset: 100,000 baris x 8 kolom
- Processed resume dataset: 69,929 baris x 7 kolom

### Inti hasil
- Wrangling berhasil menghasilkan dataset yang konsisten, terstandardisasi, dan siap untuk EDA serta pemodelan.
- Penyusutan ukuran data terutama dipengaruhi oleh deduplikasi, pemisahan tech/non-tech, dan filtering kualitas requirement summary.
- `language_signal` dipertahankan sebagai metadata kualitas, bukan sebagai filter keras.

---

## 2. Sumber Data dan Ruang Lingkup

### 2.1 Sumber data utama
- data/raw/job_listings_dataset_v3.csv
- data/raw/resume_dataset.csv

### 2.2 Target output
- data/processed/indotech_job_cleaned.csv
- data/processed/indotech_job_train.csv
- data/processed/indotech_nontech.csv
- data/processed/techtalent_profile_cleaned.csv

---

## 3. Temuan pada Tahap Assessing Data

### 3.1 Dataset lowongan kerja
Masalah utama yang diidentifikasi:
1. Invalid value pada status lowongan (`EXPIRED`).
2. Inconsistent value pada kategori pekerjaan (variasi penamaan sangat tinggi).
3. Inconsistent format pada daftar skill (`skills_top_10_names`).
4. Duplikasi data pada kombinasi tertentu (`job_id`, serta `title + company_name`).
5. Teks mentah yang masih mengandung HTML pada field deskripsi dan requirement.
6. Requirement summary yang terlalu pendek dan tidak cukup informatif untuk analisis skill.

Catatan:
- `language_signal = UNKNOWN` ditemukan pada sebagian data, tetapi tidak digunakan sebagai alasan otomatis untuk membuang row karena masih banyak row yang relevan untuk konteks tech analysis.

### 3.2 Dataset resume
Masalah utama yang diidentifikasi:
1. Adanya role non-tech pada dataset kandidat.
2. Duplikasi profil berbasis `Skills`.
3. Kolom `Name` tidak informatif untuk tujuan matching.
4. Label pendidikan belum sesuai format Indonesia.

---

## 4. Tindakan pada Tahap Cleaning Data

### 4.1 Job dataset
Langkah cleaning utama:
1. Filter status lowongan aktif (`ACTIVE`) dan buang `EXPIRED`.
2. Deduplikasi berbasis `job_id`, dilanjutkan `title + company_name`.
3. Pembersihan HTML pada `description` dan `requirement_summary`.
4. Normalisasi kategori pekerjaan menggunakan mapping.
5. Multi-signal tech detection (kategori, judul, dan skill) untuk memisahkan tech vs non-tech.
6. Normalisasi province dan salary fields.
7. Standardisasi separator dan format skill.
8. Filtering requirement summary minimum (informasi cukup untuk analisis).
9. Penandaan quality gate (`is_train_ready`) untuk kebutuhan model.

### 4.2 Resume dataset
Langkah cleaning utama:
1. Menghapus role non-tech (`Doctor`, `Mechanical Engineer`, `Embedded Engineer`).
2. Menghapus duplikasi berbasis `Skills`.
3. Menghapus kolom `Name`.
4. Normalisasi format `Skills` dan `Required_Skills`.
5. Mapping `Education` ke format Indonesia (`S1`, `S2`, `D3`).

---

## 5. Analisis Penyusutan Jumlah Data

### 5.1 Mengapa ukuran job dataset berkurang signifikan
Penyusutan job dataset dari 3,883 ke 1,679 terjadi karena kombinasi tahapan berikut:
1. Penghapusan lowongan yang tidak aktif (`EXPIRED`).
2. Deduplikasi pada level identitas lowongan.
3. Pemisahan lowongan non-tech ke dataset terpisah (`indotech_nontech.csv`).
4. Penghapusan lowongan dengan requirement summary yang tidak cukup informatif.

Kesimpulan:
- Dataset akhir memang lebih kecil, tetapi kualitas analitisnya lebih tinggi untuk use case tech matching.

### 5.2 Mengapa ukuran resume dataset berkurang
Penyusutan resume dari 100,000 ke 69,929 dipengaruhi oleh:
1. Penghapusan role non-tech.
2. Penghapusan duplikasi profil berdasarkan `Skills`.
3. Penghapusan kolom non-informatif (`Name`) pada level fitur.

---

## 6. Catatan Kebijakan Data

1. `language_signal` diperlakukan sebagai metadata kualitas dan audit, bukan filter utama.
2. Dataset non-tech disimpan, tidak dibuang, untuk kebutuhan referensi dan evaluasi lanjutan.
3. Kolom audit pipeline tech signal dipertahankan pada output job agar jejak keputusan tetap transparan.

---

## 7. Kualitas Dataset Final

### 7.1 indotech_job_cleaned.csv
- Shape: 1,679 x 34
- Missing values: 0
- Duplicate rows: 0
- Status: seluruh row `ACTIVE`

### 7.2 indotech_job_train.csv
- Shape: 1,678 x 34
- Seluruh row memenuhi quality gate training (`is_train_ready = 1`)

### 7.3 techtalent_profile_cleaned.csv
- Shape: 69,929 x 7
- Missing values: 0
- Duplicate rows: 0

---

## 8. Penutup

Proses data wrangling telah menghasilkan dataset yang:
1. Relevan dengan ruang lingkup analisis tech labor market.
2. Konsisten secara struktur dan format.
3. Siap digunakan untuk EDA, visualisasi explanatory, dan baseline pemodelan job matching.

Dokumen ini menjadi referensi formal untuk tahap analisis lanjutan dan sinkronisasi dokumentasi proyek.
