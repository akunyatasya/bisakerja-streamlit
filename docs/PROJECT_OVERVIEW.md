# Project Overview - BisaKerja Dataset

> Capstone Project - Coding Camp 2026 powered by DBS Foundation  
> Team ID: CC26-PSU263  
> Last updated: May 2026

---

## 1. Project Background

Pertumbuhan sektor teknologi di Indonesia meningkatkan kebutuhan talenta digital secara konsisten. Pada saat yang sama, terjadi tantangan dalam menyelaraskan kebutuhan skill pasar kerja dengan profil skill kandidat.

BisaKerja dikembangkan sebagai fondasi analitik untuk:
- Mengukur kesenjangan skill antara demand (lowongan) dan supply (kandidat).
- Menyusun baseline metrik kesiapan kandidat untuk job matching.
- Mendukung pipeline AI job-fit scoring yang dapat dijelaskan.

---

## 2. Problem Statement

Masalah utama yang ditangani proyek ini adalah keterbatasan visibilitas kuantitatif terhadap:
- Skill apa yang paling dibutuhkan pasar kerja tech Indonesia.
- Seberapa siap kandidat saat ini terhadap kebutuhan tersebut.
- Seberapa besar gap pada level role dan pengalaman.

---

## 3. Project Objectives

1. Mengidentifikasi skill teknis paling dominan pada lowongan tech Indonesia.
2. Mengukur coverage skill kandidat terhadap demand pasar.
3. Menganalisis distribusi kebutuhan pengalaman dari sisi lowongan.
4. Membandingkan demand role (job side) dan supply role (candidate side).
5. Menghitung metrik skill overlap untuk kebutuhan entry-level.

---

## 4. Dataset Scope

### 4.1 Job datasets
- indotech_job_cleaned.csv (1,679 x 34)
- indotech_job_train.csv (1,678 x 34)
- indotech_nontech.csv (1,395 x 31)

Keterangan:
- `indotech_job_cleaned.csv` adalah basis utama EDA untuk lowongan tech.
- `indotech_job_train.csv` adalah subset training-ready (`is_train_ready = 1`).
- `indotech_nontech.csv` disimpan sebagai referensi untuk analisis komparatif/non-tech.

### 4.2 Candidate dataset
- techtalent_profile_cleaned.csv (69,929 x 7)

Dataset ini dipakai untuk evaluasi kesiapan kandidat, analisis role distribution, dan perhitungan skill overlap.

### 4.3 Reference taxonomy
- skill_taxonomy_bisakerja_v3.csv
- job_role_taxonomy_bisakerja_v3.csv

Taxonomy digunakan untuk menjaga konsistensi normalisasi skill dan role.

---

## 5. Data Wrangling Summary

Pipeline wrangling yang digunakan:
1. Gathering data dari raw source.
2. Assessing data (missing, invalid, duplicate, inconsistent, relevansi).
3. Cleaning data (deduplikasi, text cleaning, normalisasi, filtering kualitas).
4. Multi-signal tech detection (`category`, `title`, `skills`).
5. Quality gate untuk data training.

Catatan kebijakan data:
- `status = EXPIRED` difilter keluar dari dataset utama.
- `language_signal` dipertahankan sebagai metadata kualitas (bukan filter keras).
- Penyusutan row utamanya disebabkan oleh deduplikasi, pemisahan tech/non-tech, dan filter requirement summary yang kurang informatif.

---

## 6. Business Questions

Analisis diarahkan untuk menjawab pertanyaan berikut:
1. Top skill demand dan coverage kandidat.
2. Distribusi kebutuhan pengalaman dan kesiapan kandidat entry-level.
3. Demand role paling tinggi dan proporsi kandidat yang sesuai.
4. Rata-rata skill overlap kandidat terhadap requirement lowongan entry-level.

---

## 7. Analytical Framework

Kerangka analisis proyek:
1. Data wrangling terstruktur.
2. Exploratory Data Analysis (EDA).
3. Visualization and explanatory analysis.
4. Conclusion and recommendation.
5. Baseline metrik untuk model job matching.

---

## 8. Expected Outputs

- Tabel ringkasan demand skill, demand role, dan distribusi pengalaman.
- Visualisasi untuk setiap business question.
- Kesimpulan per pertanyaan bisnis.
- Rekomendasi action item untuk peningkatan kesiapan kandidat.

---

Dokumen ini menjadi acuan tingkat proyek. Untuk detail kolom dataset, gunakan DATA_DICTIONARY.md. Untuk detail proses cleaning, gunakan DATA_WRANGLING.md.
