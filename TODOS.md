# TODO Feature Engineering - BisaKerja

Dokumen ini berisi fase implementasi feature engineering berdasarkan notebook `notebooks/data_wrangling.ipynb`, `notebooks/eda_analysis.ipynb`, serta catatan leakage pada `REPORT.md`.

Tujuan utama tahap ini adalah menyiapkan fitur yang aman untuk modeling job matching, role classification, skill gap analysis, dan dashboard insight tanpa memasukkan target, label audit, atau statistik dari data evaluasi ke dalam proses training.

---

## Status Umum

- [x] Buat notebook baru `notebooks/feature_engineering.ipynb`.
- [ ] Pisahkan artifact EDA dan artifact modeling.
- [ ] Definisikan daftar fitur yang boleh dipakai dan kolom yang wajib dikeluarkan.
- [x] Simpan output feature engineering ke folder `data/features/`.
- [ ] Dokumentasikan skema akhir di `docs/DATA_DICTIONARY.md`.

---

## Phase 0 - Scope dan Baseline Input

Tujuan: memastikan feature engineering memakai dataset processed terbaru dan definisi use case yang jelas.

- [x] Load dataset utama:
  - `data/processed/indotech_job_cleaned.csv`
  - `data/processed/indotech_job_train.csv`
  - `data/processed/techtalent_profile_cleaned.csv`
  - `data/processed/indotech_nontech.csv` jika dibutuhkan sebagai negative/reference sample.
- [x] Validasi shape, missing values, duplicate rows, dan kolom wajib.
- [x] Tetapkan use case awal:
  - job fit scoring,
  - skill gap analysis,
  - resume/job role classification,
  - dashboard analytics.
- [x] Buat konfigurasi global:
  - `RANDOM_STATE = 42`
  - path input/output,
  - daftar kolom identifier,
  - daftar kolom target,
  - daftar kolom audit/pipeline.
- [x] Catat perbedaan definisi `indotech_job_train.csv`: dataset ini adalah modeling-ready subset, bukan train split final.

Deliverable:

- [x] Section notebook "Phase 0 - Scope and Input Validation".
- [x] Ringkasan validasi dataset dalam tabel.

---

## Phase 1 - Leakage Guard dan Split Strategy

Tujuan: mencegah target leakage sebelum fitur dibuat.

- [ ] Buat daftar `EXCLUDE_COLUMNS_JOB`:
  - `job_id`
  - `is_tech`
  - `tech_signal_source`
  - `_is_tech_cat`
  - `_is_tech_title`
  - `_is_tech_skills`
  - `is_train_ready`
  - `fit_input_quality_score`
  - `fit_input_has_requirements`
  - `fit_input_has_skills`
- [ ] Buat daftar `EXCLUDE_COLUMNS_RESUME_ROLE_MODEL`:
  - `ID`
  - `Job_Role`
  - `Required_Skills`
  - fitur turunan dari `Required_Skills` jika targetnya adalah `Job_Role`.
- [ ] Untuk job dataset, pilih strategi split:
  - prioritas: time-based split menggunakan `source_posted_at`,
  - fallback: random split berbasis `job_id`.
- [ ] Untuk resume role classification, gunakan stratified split berdasarkan `Job_Role`.
- [ ] Pastikan semua transformer/statistik global hanya di-fit pada train split.
- [ ] Simpan metadata split:
  - `split`
  - `split_strategy`
  - `split_created_at`
  - `random_state`.

Deliverable:

- [ ] `data/features/job_split_metadata.csv`
- [ ] `data/features/resume_split_metadata.csv`
- [ ] Section notebook "Phase 1 - Leakage Guard and Split".

---

## Phase 2 - Normalisasi Skill dan Role

Tujuan: membuat representasi skill/role yang konsisten untuk demand, supply, dan matching.

- [ ] Implementasikan parser list skill untuk kolom:
  - job: `skills_clean`, `skills_top_10_names`, `requirements_concat`,
  - resume: `Skills`, `Required_Skills`.
- [ ] Normalisasi teks skill:
  - lowercase,
  - trim whitespace,
  - hapus duplikasi dalam satu row,
  - samakan separator menjadi list Python,
  - simpan versi canonical untuk matching.
- [ ] Jika taxonomy tersedia, mapping alias skill ke nama standar:
  - `skill_raw`,
  - `skill_standard`,
  - `category`,
  - `subcategory`.
- [ ] Normalisasi role:
  - job: `normalized_title`,
  - resume: `Job_Role`,
  - taxonomy role jika tersedia.
- [ ] Buat fitur jumlah dan kategori skill:
  - `skill_count`,
  - `unique_skill_count`,
  - `programming_skill_count`,
  - `data_skill_count`,
  - `cloud_skill_count`,
  - `security_skill_count`,
  - `soft_skill_count`.

Deliverable:

- [ ] Fungsi reusable `parse_skill_list()`.
- [ ] Fungsi reusable `normalize_skill_list()`.
- [ ] Kolom list/canonical skill pada job dan resume feature table.

---

## Phase 3 - Job Feature Engineering

Tujuan: membuat fitur numerik, kategorikal, teks, salary, lokasi, dan waktu dari lowongan kerja.

- [ ] Text features:
  - `title_len`,
  - `description_len`,
  - `requirement_len`,
  - `requirements_concat_len`,
  - `title_word_count`,
  - `description_word_count`,
  - `requirement_word_count`.
- [ ] Skill features:
  - `job_skill_count`,
  - `job_skill_diversity`,
  - `has_programming_skill`,
  - `has_cloud_skill`,
  - `has_data_skill`,
  - `has_security_skill`,
  - `has_testing_skill`.
- [ ] Salary features:
  - `salary_available`,
  - `salary_midpoint`,
  - `salary_range`,
  - `log_salary_min`,
  - `log_salary_max`,
  - `log_salary_midpoint`.
- [ ] Experience features:
  - mapping ordinal `experience_level` ke `experience_rank`,
  - `is_entry_level`,
  - `is_senior_level`.
- [ ] Work arrangement features:
  - one-hot/label encoding untuk `work_type`,
  - one-hot/label encoding untuk `employment_type`.
- [ ] Location features:
  - `province_normalized`,
  - `city_normalized`,
  - `is_jakarta_area`,
  - `is_remote_or_hybrid`.
- [ ] Date features:
  - `posted_year`,
  - `posted_month`,
  - `posted_dayofweek`,
  - `posted_recency_days` jika anchor date disepakati.
- [ ] Drop kolom audit/pipeline sebelum output modeling.

Deliverable:

- [ ] `data/features/job_features.csv`
- [ ] `data/features/job_feature_columns.json`
- [ ] Section notebook "Phase 3 - Job Features".

---

## Phase 4 - Resume Feature Engineering

Tujuan: membuat fitur kandidat yang aman untuk modeling dan analisis supply.

- [ ] Candidate skill features:
  - `candidate_skill_count`,
  - `candidate_unique_skill_count`,
  - jumlah skill per kategori taxonomy,
  - flag kategori skill utama.
- [ ] Project text features:
  - `project_count`,
  - `projects_len`,
  - `projects_word_count`,
  - indikator project AI/data/web/cloud/security jika relevan.
- [ ] Education features:
  - ordinal mapping `D3`, `S1`, `S2`,
  - one-hot encoding pendidikan jika dibutuhkan.
- [ ] Experience features:
  - ordinal mapping `Fresher`, `1-2 years`, `3-5 years`, `5+ years`,
  - `is_fresher`,
  - `is_experienced`.
- [ ] Role label handling:
  - gunakan `Job_Role` sebagai target hanya untuk role classification,
  - jangan gunakan `Required_Skills` atau fitur turunannya sebagai input model `Job_Role`.
- [ ] Simpan versi fitur berbeda:
  - safe features untuk role classification,
  - analysis features untuk skill gap/dashboard.

Deliverable:

- [ ] `data/features/resume_features_safe.csv`
- [ ] `data/features/resume_features_analysis.csv`
- [ ] `data/features/resume_feature_columns.json`
- [ ] Section notebook "Phase 4 - Resume Features".

---

## Phase 5 - Matching dan Skill Gap Features

Tujuan: membuat fitur interaksi kandidat-lowongan untuk job fit scoring dan rekomendasi upskilling.

- [ ] Definisikan pasangan kandidat-lowongan untuk eksperimen awal:
  - sampled candidate-job pairs,
  - role-based candidate-job pairs,
  - optional negative pairs.
- [ ] Buat fitur overlap skill:
  - `skill_overlap_count`,
  - `skill_overlap_ratio_candidate`,
  - `skill_overlap_ratio_job`,
  - `jaccard_skill_similarity`,
  - `missing_skill_count`,
  - `extra_skill_count`.
- [ ] Buat fitur gap per kategori:
  - `missing_programming_skill_count`,
  - `missing_data_skill_count`,
  - `missing_cloud_skill_count`,
  - `missing_security_skill_count`,
  - `missing_soft_skill_count`.
- [ ] Buat fitur alignment:
  - `experience_gap`,
  - `education_match_flag`,
  - `role_match_flag`,
  - `location_preference_match` jika tersedia.
- [ ] Buat skor baseline rule-based:
  - skill match score,
  - experience match score,
  - role/category match score,
  - total fit score 0-100.
- [ ] Pastikan fitur matching yang memakai requirement/job target tidak dipakai untuk model yang targetnya memprediksi `Job_Role`.

Deliverable:

- [ ] `data/features/matching_features_sample.csv`
- [ ] `data/features/skill_gap_features.csv`
- [ ] Section notebook "Phase 5 - Matching and Skill Gap Features".

---

## Phase 6 - Encoding, Scaling, dan Text Vectorization

Tujuan: menyiapkan fitur untuk model klasik maupun baseline yang reproducible.

- [ ] Pisahkan fitur numerik, kategorikal, boolean, dan teks.
- [ ] Fit imputer hanya pada train split.
- [ ] Fit encoder hanya pada train split.
- [ ] Fit scaler hanya pada train split.
- [ ] Untuk teks, buat baseline vectorization:
  - `TfidfVectorizer` untuk `normalized_title`,
  - `TfidfVectorizer` untuk `requirement_summary`,
  - `TfidfVectorizer` untuk `Skills` atau `Projects`.
- [ ] Simpan pipeline preprocessing sebagai artifact.
- [ ] Catat feature names hasil encoding/vectorization.

Deliverable:

- [ ] `data/features/preprocessing_config.json`
- [ ] `models/preprocessing_job.pkl` jika folder model digunakan.
- [ ] `models/preprocessing_resume.pkl` jika folder model digunakan.
- [ ] Section notebook "Phase 6 - Encoding and Preprocessing".

---

## Phase 7 - Feature Validation dan Quality Checks

Tujuan: memastikan output fitur stabil, tidak bocor, dan siap dipakai modeling.

- [ ] Cek tidak ada kolom target/audit dalam feature matrix.
- [ ] Cek missing values setelah feature engineering.
- [ ] Cek duplicate rows pada level identifier atau pair identifier.
- [ ] Cek nilai tak valid:
  - salary negatif,
  - skill count negatif,
  - overlap ratio di luar 0-1,
  - log salary invalid.
- [ ] Cek distribusi fitur penting:
  - `skill_count`,
  - `salary_midpoint`,
  - `experience_rank`,
  - `skill_overlap_ratio_job`.
- [ ] Cek drift sederhana antar split untuk fitur kunci.
- [ ] Buat laporan ringkas validasi fitur.

Deliverable:

- [ ] `reports/FEATURE_ENGINEERING_REPORT.md`
- [ ] Tabel validasi fitur di notebook.
- [ ] Section notebook "Phase 7 - Feature Validation".

---

## Phase 8 - Output Final dan Integrasi

Tujuan: menghasilkan artifact final yang mudah dipakai tahap modeling dan dashboard.

- [ ] Simpan dataset fitur final:
  - `data/features/job_features.csv`
  - `data/features/resume_features_safe.csv`
  - `data/features/resume_features_analysis.csv`
  - `data/features/matching_features_sample.csv`
  - `data/features/skill_gap_features.csv`
- [ ] Simpan daftar fitur:
  - `data/features/job_feature_columns.json`
  - `data/features/resume_feature_columns.json`
  - `data/features/matching_feature_columns.json`
- [ ] Update dokumentasi:
  - `docs/DATA_DICTIONARY.md`
  - `README.md` bagian pipeline jika diperlukan.
- [ ] Tambahkan catatan batasan:
  - `Required_Skills` tidak boleh menjadi fitur input untuk prediksi `Job_Role`.
  - `indotech_job_train.csv` bukan split training final.
  - kolom audit pipeline hanya untuk analisis/debug.
- [ ] Siapkan checklist transisi ke modeling:
  - target jelas,
  - split tersedia,
  - preprocessing fit-only-on-train,
  - feature matrix bebas leakage.

Deliverable:

- [ ] Feature engineering notebook selesai.
- [ ] Dataset fitur tersimpan.
- [ ] Dokumentasi dan report diperbarui.

---

## Prioritas Implementasi

1. Phase 1 - Leakage Guard dan Split Strategy.
2. Phase 2 - Normalisasi Skill dan Role.
3. Phase 3 - Job Feature Engineering.
4. Phase 4 - Resume Feature Engineering.
5. Phase 5 - Matching dan Skill Gap Features.
6. Phase 7 - Feature Validation.
7. Phase 8 - Output Final dan Integrasi.
8. Phase 6 - Encoding, Scaling, dan Text Vectorization, dikerjakan setelah fitur tabular dasar stabil.

---

## Catatan Keputusan

- Feature engineering untuk EDA dan modeling harus dipisahkan karena EDA boleh memakai keseluruhan data, sedangkan modeling wajib memakai split dan transformer yang di-fit hanya pada train.
- Fitur turunan `Required_Skills` berguna untuk skill gap analysis, tetapi berisiko leakage untuk role classification.
- Kolom audit seperti `_is_tech_cat`, `is_tech`, dan `is_train_ready` tetap berguna untuk inspeksi pipeline, tetapi tidak boleh otomatis masuk ke feature matrix.
- Baseline rule-based fit score boleh dibuat sebagai pembanding awal, tetapi harus dibedakan dari model prediktif yang dievaluasi dengan split.
