# Data Dictionary - BisaKerja

> Capstone Project - Coding Camp 2026 powered by DBS Foundation  
> Team ID: CC26-PSU263  
> Versi dokumen ini disesuaikan dengan dataset processed terbaru (Mei 2026).

---

## Ringkasan Dataset

| Dataset | Shape | Missing Values | Duplicate Rows | Keterangan |
|---|---:|---:|---:|---|
| indotech_job_cleaned.csv | 1,679 x 34 | 0 | 0 | Lowongan tech aktif untuk analisis utama |
| indotech_job_train.csv | 1,678 x 34 | 0 | 0 | Subset training-ready (`is_train_ready = 1`) |
| indotech_nontech.csv | 1,395 x 31 | 1,905 | 0 | Lowongan non-tech hasil pemisahan multi-signal |
| techtalent_profile_cleaned.csv | 69,929 x 7 | 0 | 0 | Profil kandidat tech terstandardisasi |
| skill_taxonomy_bisakerja_v3.csv | 576 x 4 (usable) | 0 | - | Referensi normalisasi skill |
| job_role_taxonomy_bisakerja_v3.csv | 119 x 4 | - | - | Referensi normalisasi role |

---

## 1) indotech_job_cleaned.csv

### Deskripsi
Dataset lowongan kerja tech aktif di Indonesia setelah proses gathering, assessing, cleaning, dan quality gate.

### Catatan penting
- Semua row berstatus `ACTIVE`.
- `language_signal` tidak dipakai sebagai filter keras; nilai `UNKNOWN` masih ada sebagai metadata kualitas.
- Kolom debug multi-signal (`_is_tech_cat`, `_is_tech_title`, `_is_tech_skills`) masih disimpan untuk audit pipeline.

### Kolom

#### Identifier
| Kolom | Tipe | Deskripsi |
|---|---|---|
| job_id | string | ID unik lowongan (UUID) |
| company_name | string | Nama perusahaan |

#### Job information
| Kolom | Tipe | Deskripsi |
|---|---|---|
| title | string | Judul lowongan asli |
| normalized_title | string | Judul lowongan yang telah dinormalisasi |
| category | string | Kategori pekerjaan setelah normalisasi |
| work_type | string | Jenis pola kerja (onsite/hybrid/remote) |
| employment_type | string | Jenis kontrak kerja |
| experience_level | string | Tingkat pengalaman yang diminta |

#### Text fields
| Kolom | Tipe | Deskripsi |
|---|---|---|
| description | string | Deskripsi pekerjaan (HTML-stripped) |
| requirement_summary | string | Ringkasan persyaratan (HTML-stripped) |
| requirements_concat | string | Gabungan teks persyaratan |

#### Location and salary
| Kolom | Tipe | Deskripsi |
|---|---|---|
| province | string | Provinsi lowongan (sudah dinormalisasi) |
| city | string | Kota lokasi lowongan |
| salary_min | float64 | Gaji minimum (IDR), 0 jika tidak tersedia |
| salary_max | float64 | Gaji maksimum (IDR), 0 jika tidak tersedia |
| salary_currency | string | Mata uang gaji |
| salary_display | string | Teks gaji dari sumber |
| has_salary_info | int64 | Flag ketersediaan salary pada sumber |

#### Skill and metadata
| Kolom | Tipe | Deskripsi |
|---|---|---|
| skills_top_10_names | string | Skill mentah hasil scraping (separator asal) |
| skills_clean | string | Skill yang telah distandardisasi separator dan spasi |
| skills_count_total | int64 | Jumlah skill pada lowongan |
| language_signal | string | Sinyal bahasa posting (`EN`, `ID`, `MIXED`, `UNKNOWN`) |
| source_posted_at | datetime/string | Waktu posting dari sumber |
| status | string | Status lowongan |

#### Quality flags
| Kolom | Tipe | Deskripsi |
|---|---|---|
| fit_input_quality_score | int64 | Skor kualitas input |
| fit_input_has_requirements | int64 | Flag ada/tidaknya requirement |
| fit_input_has_skills | int64 | Flag ada/tidaknya skills |
| description_length_chars | int64 | Panjang deskripsi |

#### Pipeline labels
| Kolom | Tipe | Deskripsi |
|---|---|---|
| _is_tech_cat | bool | Sinyal tech dari kategori |
| _is_tech_title | bool | Sinyal tech dari judul |
| _is_tech_skills | bool | Sinyal tech dari skill |
| is_tech | bool | Label akhir tech/non-tech |
| tech_signal_source | string | Jejak sumber sinyal tech |
| is_train_ready | int64 | Flag siap training model |

---

## 2) indotech_job_train.csv

### Deskripsi
Subset dari `indotech_job_cleaned.csv` yang hanya berisi row dengan `is_train_ready = 1`.

### Catatan
- Skema kolom identik dengan `indotech_job_cleaned.csv`.
- Digunakan untuk eksperimen training model job matching.

---

## 3) indotech_nontech.csv

### Deskripsi
Dataset lowongan non-tech yang dipisahkan saat multi-signal tech detection.

### Catatan
- Dipertahankan sebagai data referensi, negative sample, atau analisis lintas domain di masa depan.
- Memiliki kolom audit tech signal (`_is_tech_cat`, `_is_tech_title`, `_is_tech_skills`, `is_tech`, `tech_signal_source`).
- Missing values masih ada karena file ini bukan target utama quality gate training.

### Kolom utama
Skema inti mengikuti lowongan kerja (identifier, informasi job, teks, lokasi, salary, metadata) ditambah kolom audit signal tech.

---

## 4) techtalent_profile_cleaned.csv

### Deskripsi
Dataset profil kandidat tech untuk analisis supply kandidat dan evaluasi skill overlap.

### Kolom
| Kolom | Tipe | Deskripsi |
|---|---|---|
| ID | int64 | ID unik kandidat |
| Skills | string | Daftar skill kandidat (comma-separated) |
| Projects | string | Daftar proyek kandidat |
| Education | string | Pendidikan tertinggi (sudah dipetakan ke S1/S2/D3) |
| Experience | string | Rentang pengalaman |
| Job_Role | string | Role kandidat |
| Required_Skills | string | Skill requirement role kandidat |

### Catatan
- Role non-tech sudah dikeluarkan.
- Kolom `Name` sudah dihapus karena tidak informatif.

---

## 5) skill_taxonomy_bisakerja_v3.csv

### Deskripsi
Tabel referensi untuk memetakan alias skill mentah ke skill standar.

### Kolom usable
| Kolom | Tipe | Deskripsi |
|---|---|---|
| skill_raw | string | Bentuk skill mentah/alias |
| skill_standard | string | Nama skill standar |
| category | string | Kategori skill |
| subcategory | string | Subkategori skill |

### Catatan
Abaikan kolom artifact seperti `Unnamed:*` jika ada pada file sumber.

---

## 6) job_role_taxonomy_bisakerja_v3.csv

### Deskripsi
Tabel referensi standardisasi role pekerjaan.

### Kolom
| Kolom | Tipe | Deskripsi |
|---|---|---|
| role_raw | string | Bentuk role mentah |
| role_standard | string | Role standar |
| role_category | string | Kategori role |
| notes | string/nullable | Catatan tambahan (opsional) |

---

## Definisi Operasional Singkat

- Skill demand: frekuensi skill pada lowongan.
- Skill supply: frekuensi skill pada profil kandidat.
- Skill overlap: irisan skill kandidat terhadap requirement job.
- Training-ready row: row job yang memenuhi quality gate untuk pemodelan.

---

Dokumen ini harus diperbarui setiap kali pipeline cleaning mengubah shape, skema, atau definisi quality gate dataset.
