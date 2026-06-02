# BisaKerja Dataset Documentation

> **Capstone Project — Coding Camp 2026 powered by DBS Foundation**
> Team ID: CC26-PSU263 | Theme: Future-Ready Work & Economy

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Dataset Files](#dataset-files)
- [Data Sources](#data-sources)
- [Dataset Shapes](#dataset-shapes)
- [Column Summaries](#column-summaries)
- [Target Variables](#target-variables)
- [Data Cleaning Summary](#data-cleaning-summary)
- [Potential Use Cases](#potential-use-cases)
- [Known Limitations](#known-limitations)
- [Data Dictionary](#data-dictionary)

---

## Project Overview

**BisaKerja** is an AI-powered Career Decision Engine designed to address Indonesia's labor market inefficiencies, particularly the horizontal skill mismatch affecting 73.97% of young vocational graduates (BPS, 2025). The platform provides:

- **Job Fit Scoring** — An AI model that calculates a 0–100 compatibility score between a candidate profile and a job listing.
- **Skill Gap Analysis** — Identifies missing competencies and prioritizes upskilling recommendations.
- **Explainable AI (XAI)** — Transparent scoring breakdown covering skill match, experience alignment, and preference fit.

This repository contains the cleaned and processed datasets used for Exploratory Data Analysis (EDA), model training, and Streamlit dashboard deployment.

---

## Repository Structure

```
data_cleaned/
├── indotech_job_cleaned.csv          # Tech job listings — full EDA & Streamlit dataset
├── indotech_job_train.csv            # Tech job listings — AI model training subset
├── indotech_nontech.csv              # Non-tech job listings — reference/negative samples
├── job_role_taxonomy_bisakerja_v3.csv # Job role normalization mapping table
├── skill_taxonomy_bisakerja_v3.csv   # Skill normalization and categorization table
└── techtalent_profile_cleaned.csv    # Candidate profile dataset for model training
```

---

## Dataset Files

| File | Purpose | Rows | Columns |
|------|---------|------|---------|
| `indotech_job_cleaned.csv` | Primary tech job dataset for EDA, visualization, and Streamlit | 698 | 31 |
| `indotech_job_train.csv` | Filtered training-ready subset for AI model (identical to cleaned in this version) | 698 | 31 |
| `indotech_nontech.csv` | Non-tech jobs retained for reference and negative sample analysis | 1,201 | 32 |
| `job_role_taxonomy_bisakerja_v3.csv` | Mapping table: raw role names → standardized role names | 119 | 4 |
| `skill_taxonomy_bisakerja_v3.csv` | Mapping table: raw skill aliases → standardized skill names + categories | 576 | 4 (usable) |
| `techtalent_profile_cleaned.csv` | Candidate profiles with skills, experience, education, and required skills | 69,929 | 7 |

---

## Data Sources

### IndoTech-Job Dataset (`indotech_job_*`)
- **Source:** Web-scraped from Indonesian job platforms — Kalibrr, KitaLulus, and Dealls
- **Collection Period:** April–May 2026
- **Original Size:** 2,099 rows before cleaning
- **Language:** Indonesian (ID) and Mixed (ID + EN)

### TechTalent-Profile Dataset (`techtalent_profile_cleaned.csv`)
- **Source:** Synthetic candidate profile dataset
- **⚠️ Assumption:** Based on profile structure (B.Tech, M.Tech, MBBS education labels prior to remapping), the source data reflects a global/South Asian talent profile distribution. Education labels have been remapped to the Indonesian format (S1, S2, D3) for consistency.
- **Original Size:** 100,000 rows before cleaning

### Taxonomy Files
- **Source:** Manually curated by the BisaKerja team to standardize skill and role naming conventions found in Indonesian job listings.

---

## Dataset Shapes

| Dataset | Rows | Columns | Missing Values |
|---------|------|---------|---------------|
| `indotech_job_cleaned.csv` | 698 | 31 | 0 |
| `indotech_job_train.csv` | 698 | 31 | 0 |
| `indotech_nontech.csv` | 1,201 | 32 | ~1,393 (category, salary, date) |
| `job_role_taxonomy_bisakerja_v3.csv` | 119 | 4 | 103 (notes col, intentional) |
| `skill_taxonomy_bisakerja_v3.csv` | 576 | 4 | 0 (3 artifact columns excluded) |
| `techtalent_profile_cleaned.csv` | 69,929 | 7 | 0 |

---

## Column Summaries

### `indotech_job_cleaned.csv` / `indotech_job_train.csv`

Identical schema. The `_train` file is the AI-model-ready subset filtered by `is_train_ready = 1`.

| Group | Columns |
|-------|---------|
| **Identifier** | `job_id`, `company_name` |
| **Job Info** | `title`, `normalized_title`, `category`, `work_type`, `employment_type`, `experience_level` |
| **Text Content** | `description`, `requirement_summary`, `requirements_concat` |
| **Location** | `province`, `city` |
| **Salary** | `salary_min`, `salary_max`, `salary_currency`, `salary_display`, `has_salary_info` |
| **Skills** | `skills_top_10_names`, `skills_clean`, `skills_count_total` |
| **Metadata** | `language_signal`, `source_posted_at`, `status` |
| **Quality Flags** | `fit_input_quality_score`, `fit_input_has_requirements`, `fit_input_has_skills`, `description_length_chars` |
| **Pipeline Labels** | `is_tech`, `tech_signal_source`, `is_train_ready` |

**Category distribution:**

| Category | Count | % |
|----------|-------|---|
| IT & Software | 506 | 72.5% |
| Data & Analytics | 40 | 5.7% |
| Product Management | 37 | 5.3% |
| QA & Testing | 32 | 4.6% |
| Others (minor) | 83 | 11.9% |

**Experience level distribution:**

| Level | Count | % |
|-------|-------|---|
| ENTRY_LEVEL | 230 | 33.0% |
| JUNIOR | 208 | 29.8% |
| MID_LEVEL | 165 | 23.6% |
| SENIOR | 66 | 9.5% |
| LEAD | 29 | 4.2% |

---

### `techtalent_profile_cleaned.csv`

| Group | Columns |
|-------|---------|
| **Identifier** | `ID` |
| **Profile Content** | `Skills`, `Projects`, `Required_Skills` |
| **Demographics** | `Education`, `Experience` |
| **Target** | `Job_Role` |

**Job role distribution (balanced):**

| Job Role | Count |
|----------|-------|
| Cloud Engineer | 10,078 |
| Data Scientist | 10,067 |
| Cybersecurity Analyst | 10,031 |
| Web Developer | 9,975 |
| Business Analyst | 9,963 |
| Backend Developer | 9,945 |
| ML Engineer | 9,870 |

**Experience distribution:**

| Level | Count |
|-------|-------|
| 5+ years | 17,569 |
| Fresher | 17,503 |
| 3–5 years | 17,445 |
| 1–2 years | 17,412 |

---

### `skill_taxonomy_bisakerja_v3.csv`

576 skill entries across 18 categories including: Programming Language, Frontend/Backend Framework, AI/ML, Data, DevOps, Cloud, Testing, Security, Indonesian Term, and Soft Skill.

### `job_role_taxonomy_bisakerja_v3.csv`

119 role mappings across 19 role categories including: Software Engineering, Data, AI/ML, Quality Assurance, Design, Management, DevOps, Security, and IT Operations.

---

## Target Variables

### For AI Job Fit Scoring Model
- **Primary input (job side):** `skills_clean`, `requirement_summary`, `requirements_concat`, `experience_level`, `category`
- **Primary input (candidate side):** `Skills`, `Required_Skills`, `Experience`, `Job_Role`
- **Target output:** Fit score (0–100) — *computed, not stored in dataset*

### For Job Role Classification (Resume Dataset)
- **Target variable:** `Job_Role` in `techtalent_profile_cleaned.csv`
- **Type:** Multi-class classification (7 classes)
- **Balance:** Near-perfectly balanced (~10,000 per class)

### For Skill Gap Analysis
- **Derived from:** Difference between `Required_Skills` (job) and `Skills` (candidate)
- **Output:** List of missing skills ranked by frequency in `skill_taxonomy`

---

## Data Cleaning Summary

The following cleaning steps were applied to produce the files in this folder. All cleaning was performed in `notebook.ipynb`.

### `indotech_job_cleaned.csv`

| Step | Action | Rows Affected |
|------|--------|--------------|
| Fix 1 | Removed `EXPIRED` status and `UNKNOWN` language signal entries | −5 rows |
| Fix 2 | Deduplicated by `job_id`, then by `title + company_name` (kept newest) | −51 rows |
| Fix 3 | Stripped all HTML tags from `description` and `requirement_summary` using BeautifulSoup | 698 rows cleaned |
| Fix 4 | Applied `CATEGORY_MAPPING` (75+ entries) to unify 204 category variants into standardized names | All rows |
| Fix 4 | Multi-signal tech detection: `is_tech = is_tech_cat OR is_tech_title`; non-tech rows saved separately | 1,201 rows separated |
| Fix 4b | Inferred `category` from `normalized_title` for 33 rows where category remained null after mapping | 33 rows filled |
| Fix 5 | Standardized `province` names (e.g., `Daerah Khusus Ibukota Jakarta` → `DKI Jakarta`) | ~10 mappings |
| Fix 6 | Flagged salary availability (`has_salary_info`); replaced `salary_min = 1` with 0; filled null salary with 0 | ~399 rows |
| Fix 7 | Parsed `source_posted_at` to datetime; filled nulls with median date | ~285 rows |
| Fix 8 | Standardized `skills_top_10_names` separator from pipe `\|` to comma `,` → stored in `skills_clean` | All rows |
| Fix 9 | Removed rows where `requirement_summary` < 50 characters | ~18 rows |
| Fix 10 | Labeled `is_train_ready = 1` for rows meeting quality gate: `fit_input_quality_score ≥ 60`, `skills_count_total ≥ 1`, `description_length_chars ≥ 100` | 698 flagged |

**Raw → Cleaned:** 2,099 → 698 tech rows + 1,201 non-tech rows

### `techtalent_profile_cleaned.csv`

| Step | Action | Rows Affected |
|------|--------|--------------|
| Fix 11 | Removed non-tech job roles: Doctor, Mechanical Engineer, Embedded Engineer | −30,071 rows |
| Fix 12 | Dropped exact duplicate `Skills` entries; removed uninformative `Name` column (99.8% duplicate) | −76 rows |
| Fix 13 | Cleaned `Skills` and `Required_Skills`: stripped whitespace, normalized comma separators | All rows |
| Fix 14 | Mapped India-centric education labels to Indonesian format (B.Tech → S1, M.Tech → S2, Diploma → D3) | All rows |

**Raw → Cleaned:** 100,000 → 69,929 rows

### Taxonomy Files
- Curated manually; no automated cleaning applied.
- `skill_taxonomy`: 3 fully-empty artifact columns (`Unnamed: 4`, `Unnamed: 5`, `Unnamed: 6`) present — **exclude from analysis**.
- `job_role_taxonomy`: `notes` column is 86.6% null by design (optional field).

---

## Potential Use Cases

1. **Job Fit Scoring** — Train a similarity model (cosine similarity, BERT embedding, or deep learning) to score candidate-job compatibility using `skills_clean` and `Required_Skills`.
2. **Skill Gap Analysis** — Compare `Skills` vs `Required_Skills` to identify top missing competencies per job category.
3. **Job Role Classification** — Build a multi-class classifier on `techtalent_profile_cleaned.csv` to predict suitable job roles from candidate profiles.
4. **Salary Range Prediction** — Predict salary range from `experience_level`, `category`, `province`, and `skills_clean` (limited by 57.2% undisclosed salaries).
5. **Labor Market EDA** — Analyze in-demand skills, geographic demand concentration, and experience-level distribution in Indonesia's tech sector (May 2026 snapshot).
6. **Streamlit Dashboard** — Power live analytics and recommendation features for the BisaKerja web application.

---

## Known Limitations

| # | Limitation | Affected Dataset | Impact |
|---|-----------|-----------------|--------|
| 1 | **Salary non-disclosure is high** — 57.2% of tech jobs have `salary_min = 0` (not disclosed) | `indotech_job_cleaned` | Salary prediction models will have limited coverage |
| 2 | **Category imbalance** — IT & Software dominates at 72.5%; rare categories have <10 rows | `indotech_job_cleaned` | Models may underperform for minority categories |
| 3 | **Geographic concentration** — 55.8% of jobs are in DKI Jakarta / Jakarta Raya | `indotech_job_cleaned` | Results may not generalize well to other Indonesian regions |
| 4 | **Temporal snapshot** — Data collected in April–May 2026; skill demand may shift | `indotech_job_cleaned` | Requires periodic re-scraping for production deployment |
| 5 | **Synthetic resume dataset** — `techtalent_profile_cleaned` is synthetically generated; does not reflect actual Indonesian candidate distributions | `techtalent_profile_cleaned` | Matching model trained on this data may not generalize to real resumes |
| 6 | **Non-tech category null rate** — 64.5% of non-tech rows have null `category` | `indotech_nontech` | Limits usability of non-tech data for category-level analysis |
| 7 | **Skill taxonomy coverage** — The 576 entries may not cover all emerging or niche tech skills | `skill_taxonomy` | Some skills in job listings may remain unmapped |
| 8 | **Artifact columns in skill taxonomy** — Three `Unnamed` columns are fully empty CSV artifacts | `skill_taxonomy_bisakerja_v3` | Must be excluded before loading into analysis pipelines |
| 9 | **`indotech_job_cleaned` = `indotech_job_train`** — Both files are currently identical (all 698 rows meet quality gate) | Both | The train/EDA split provides no additional filtering at this scale |

---

## Data Dictionary

See [`DATA_DICTIONARY.md`](./DATA_DICTIONARY.md) for the full column-by-column reference.
