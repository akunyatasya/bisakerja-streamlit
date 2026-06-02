"""
BisaKerja Dashboard — EDA & Explanatory Analysis
Capstone Project - Coding Camp 2026 powered by DBS Foundation
Team ID: CC26-PSU263
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import numpy as np
import os
import base64

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BisaKerja · Tech Job Market Dashboard",
    page_icon="assets/logo_bisakerja.png" if os.path.exists(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo_bisakerja.png")
    ) else "💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS — perbaiki warna teks tabel & styling umum ──────────────────
st.markdown("""
<style>
/* Tabel Streamlit: teks lebih gelap & jelas */
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] th,
[data-testid="stDataFrameResizable"] td,
[data-testid="stDataFrameResizable"] th {
    color: #1E293B !important;
    font-size: 0.88rem !important;
}
[data-testid="stDataFrame"] thead th {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    font-weight: 700 !important;
}
/* Sidebar nav lebih rapi */
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.92rem !important;
    color: #1E293B !important;
    padding: 4px 0;
}
/* Judul halaman konsisten */
h1 { color: #1E293B !important; font-size: 1.7rem !important; }
h2 { color: #1E293B !important; }
h3 { color: #374151 !important; }
h4 { color: #374151 !important; }
/* Metric card konsisten */
.metric-card p { color: #1E293B !important; }
/* Filter container */
.filter-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Color Palette ──────────────────────────────────────────────────────────
COLORS = {
    "primary":   "#2563EB",
    "secondary": "#7C3AED",
    "accent":    "#059669",
    "warning":   "#D97706",
    "danger":    "#DC2626",
    "light":     "#F1F5F9",
    "text":      "#1E293B",
}
PALETTE_BLUE   = px.colors.sequential.Blues[2:]
PALETTE_PURPLE = px.colors.sequential.Purples[2:]
PALETTE_TEAL   = px.colors.sequential.Teal[2:]
PALETTE_CAT    = px.colors.qualitative.Bold

# ─── Data Paths ─────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
ASSETS_DIR  = os.path.join(BASE_DIR, "assets")

JOB_PATH    = os.path.join(PROJECT_DIR, "data", "processed", "indotech_job_cleaned.csv")
TALENT_PATH = os.path.join(PROJECT_DIR, "data", "processed", "techtalent_profile_cleaned.csv")
SKILL_TAX   = os.path.join(PROJECT_DIR, "data", "external", "skill_taxonomy_bisakerja_v3.csv")
ROLE_TAX    = os.path.join(PROJECT_DIR, "data", "external", "job_role_taxonomy_bisakerja_v3.csv")
LOGO_PATH   = os.path.join(ASSETS_DIR, "logo_bisakerja.png")

# ─── Helper: logo loader ─────────────────────────────────────────────────────
def get_logo_html(height=100):
    """Return <img> tag dari file logo, fallback ke teks jika tidak ada."""
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = LOGO_PATH.rsplit(".", 1)[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg"
        return f"<img src='data:{mime};base64,{b64}' height='{height}' style='margin-bottom:4px'/>"
    else:
        return "<span style='font-size:2rem;'>💼</span>"

# ─── Data Loading ───────────────────────────────────────────────────────────
NOISE_TERMS = {
    "EXPIRES_SOON", "Akan segera berakhir", "Jadilah pelamar pertama",
    "EARLY_APPLICANT", "Programming", "Effective Communication",
    "null", "NULL", "",
}

@st.cache_data(show_spinner="Memuat data lowongan kerja…")
def load_jobs():
    return pd.read_csv(JOB_PATH)

@st.cache_data(show_spinner="Memuat data profil kandidat…")
def load_talent():
    return pd.read_csv(TALENT_PATH)

@st.cache_data(show_spinner="Memuat skill taxonomy…")
def load_skill_tax():
    df = pd.read_csv(SKILL_TAX)[["skill_raw", "skill_standard", "category", "subcategory"]]
    df = df.dropna(subset=["skill_raw", "skill_standard"])
    return dict(zip(df["skill_raw"].str.strip(), df["skill_standard"].str.strip()))

# ─── Utility Functions ──────────────────────────────────────────────────────
def parse_skills(text, skill_map=None):
    if pd.isna(text):
        return []
    skills = []
    for x in str(text).split(","):
        x = x.strip()
        if not x or x in NOISE_TERMS:
            continue
        if skill_map:
            x = skill_map.get(x, x)
        skills.append(x)
    return skills

def normalize_category(cat):
    if pd.isna(cat):
        return "Lainnya"
    cat = cat.strip()
    mapping = {
        "IT & Software": "IT & Software",
        "Technology": "IT & Software",
        "Information Technology & Communications": "IT & Software",
        "Information Technology & Communication": "IT & Software",
        "Information Technology": "IT & Software",
        "Data & Analytics": "Data & Analytics",
        "QA & Testing": "QA & Testing",
        "Product Management": "Product Management",
        "Frontend/Mobile Development": "Frontend & Mobile",
        "Design & UX": "Design & UX",
        "Design": "Design & UX",
        "Operation & Technical Support": "IT Support & Ops",
        "Sains & Teknologi": "IT & Software",
        "Business Analyst": "Business & Analytics",
    }
    return mapping.get(cat, "Lainnya")

def province_normalize(p):
    if pd.isna(p):
        return "Tidak Diketahui"
    p = str(p).strip()
    if p in {"DKI Jakarta", "Jakarta Raya", "Jakarta"}:
        return "DKI Jakarta"
    return p

# ─── Computed Data ───────────────────────────────────────────────────────────
@st.cache_data
def compute_all():
    jobs   = load_jobs()
    talent = load_talent()
    skill_map = load_skill_tax()

    jobs["cat_group"]      = jobs["category"].apply(normalize_category)
    jobs["province_norm"]  = jobs["province"].apply(province_normalize)

    # Talent skill sets
    talent_skill_set = set()
    for s in talent["Skills"].dropna():
        for sk in s.split(","):
            talent_skill_set.add(sk.strip())
    talent["skill_list"] = talent["Skills"].apply(
        lambda x: [s.strip() for s in str(x).split(",") if s.strip()]
    )
    talent_skill_map_lower = {s.lower(): s for s in talent_skill_set}
    talent_skill_counter   = Counter()
    for sl in talent["skill_list"]:
        talent_skill_counter.update(sl)

    # Job skill counts
    job_skill_counter = Counter()
    for s in jobs["skills_clean"].dropna():
        for sk in parse_skills(s, skill_map):
            job_skill_counter[sk] += 1

    top_job_skills_df = pd.DataFrame(
        job_skill_counter.most_common(20), columns=["skill", "demand_count"]
    )

    # Supply % per top skill
    total_talent_n = len(talent)
    supply_rows = []
    for _, row in top_job_skills_df.iterrows():
        jsk    = row["skill"]
        demand = row["demand_count"]
        match  = talent_skill_map_lower.get(jsk.lower())
        supply_cnt = talent_skill_counter.get(match, 0) if match else 0
        supply_pct = supply_cnt / total_talent_n * 100 if match else 0.0
        supply_rows.append({
            "skill": jsk, "demand_count": demand,
            "supply_count": supply_cnt, "supply_pct": round(supply_pct, 1),
            "matched": match is not None,
        })
    supply_df = pd.DataFrame(supply_rows)

    # Experience level distribution
    exp_order = ["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"]
    exp_dist  = (
        jobs["experience_level"].value_counts()
        .reindex(exp_order, fill_value=0).reset_index()
    )
    exp_dist.columns = ["level", "count"]
    exp_dist["pct"] = (exp_dist["count"] / exp_dist["count"].sum() * 100).round(1)

    # Entry-level skill readiness
    entry_jobs = jobs[jobs["experience_level"] == "ENTRY_LEVEL"]
    entry_skill_counter = Counter()
    for s in entry_jobs["skills_clean"].dropna():
        entry_skill_counter.update(parse_skills(s, skill_map))
    top_entry_skills = [s for s, _ in entry_skill_counter.most_common(10)]

    entry_candidates  = talent[talent["Experience"].isin(["Fresher", "1-2 years"])]
    total_entry_cand  = len(entry_candidates)
    entry_overlap_rows = []
    for sk in top_entry_skills:
        match = talent_skill_map_lower.get(sk.lower())
        cnt   = entry_candidates["skill_list"].apply(lambda sl: match in sl).sum() if match else 0
        pct   = cnt / total_entry_cand * 100 if match else 0.0
        entry_overlap_rows.append({
            "skill": sk, "entry_job_count": entry_skill_counter[sk],
            "candidate_pct": round(pct, 1), "matched": match is not None,
        })
    entry_skill_df = pd.DataFrame(entry_overlap_rows)

    # Role demand & supply
    role_demand = (
        jobs["normalized_title"].value_counts().head(15).reset_index()
    )
    role_demand.columns = ["role", "demand"]

    talent_role_supply = talent["Job_Role"].value_counts().reset_index()
    talent_role_supply.columns = ["role", "supply_count"]
    talent_role_supply["supply_pct"] = (
        talent_role_supply["supply_count"] / total_talent_n * 100
    ).round(1)

    # Skill overlap — entry-level candidates vs entry-level jobs
    entry_job_skill_set = set(top_entry_skills)
    overlap_list = []
    for _, row in entry_candidates.iterrows():
        cand_norm = set(row["skill_list"])
        overlap   = (
            len(cand_norm.intersection(entry_job_skill_set)) /
            len(entry_job_skill_set) * 100
        ) if entry_job_skill_set else 0.0
        overlap_list.append({
            "role": row["Job_Role"], "experience": row["Experience"],
            "overlap_pct": round(overlap, 1),
        })
    overlap_df = pd.DataFrame(overlap_list)
    overlap_by_role = (
        overlap_df.groupby("role")["overlap_pct"]
        .agg(["mean", "median", "count"]).reset_index()
    )
    overlap_by_role.columns = ["role", "mean_overlap", "median_overlap", "candidate_count"]
    overlap_by_role["mean_overlap"] = overlap_by_role["mean_overlap"].round(1)
    overlap_by_role = overlap_by_role.sort_values("mean_overlap", ascending=False)

    # Skill per category
    cat_skill_map_data = {}
    for _, row in jobs.iterrows():
        cat    = row["cat_group"]
        skills = parse_skills(row["skills_clean"], skill_map)
        if cat not in cat_skill_map_data:
            cat_skill_map_data[cat] = Counter()
        cat_skill_map_data[cat].update(skills)

    # Work type & province
    work_type_dist = jobs["work_type"].value_counts().reset_index()
    work_type_dist.columns = ["work_type", "count"]
    work_type_dist["pct"] = (work_type_dist["count"] / work_type_dist["count"].sum() * 100).round(1)

    prov_dist = jobs["province_norm"].value_counts().head(12).reset_index()
    prov_dist.columns = ["province", "count"]

    # Salary
    salary_df = jobs[jobs["salary_min"] > 1_000_000].copy()
    salary_df["salary_min_m"] = salary_df["salary_min"] / 1_000_000
    salary_df["salary_max_m"] = salary_df["salary_max"] / 1_000_000

    # Skill per experience level
    exp_skill_map_data = {}
    for level in exp_order:
        subset = jobs[jobs["experience_level"] == level]
        c = Counter()
        for s in subset["skills_clean"].dropna():
            c.update(parse_skills(s, skill_map))
        exp_skill_map_data[level] = [{"skill": sk, "count": cnt} for sk, cnt in c.most_common(8)]

    return {
        "jobs": jobs, "talent": talent,
        "supply_df": supply_df, "exp_dist": exp_dist,
        "entry_skill_df": entry_skill_df,
        "talent_role_supply": talent_role_supply,
        "role_demand": role_demand,
        "overlap_df": overlap_df, "overlap_by_role": overlap_by_role,
        "cat_skill_map": cat_skill_map_data,
        "work_type_dist": work_type_dist, "prov_dist": prov_dist,
        "salary_df": salary_df,
        "exp_skill_map": exp_skill_map_data,
        "total_talent": total_talent_n,
        "total_entry_cand": total_entry_cand,
        "job_skill_counter": job_skill_counter,
    }

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_html = get_logo_html(height=100)
    st.markdown(
        f"""
        <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
            {logo_html}
            <p style='margin:0; color:FFFFFF; font-size:0.78rem; font-weight:900;'>Tech Job Market &middot; Indonesia 2026 </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("<p style='font-size:0.8rem;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px'>Navigasi</p>", unsafe_allow_html=True)
    page = st.radio(
        "Pilih halaman:",
        [
            "Overview",
            "Skill: Demand vs Supply",
            "Experience Level",
            "Job Role & Kandidat",
            "Skill Overlap",
            "Skill per Kategori",
            "Lokasi & Work Type",
            "Analisis Gaji",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Capstone Project · CC26-PSU263")
    st.caption("Coding Camp 2026 by DBS Foundation")

# ─── Load All Data ───────────────────────────────────────────────────────────
data             = compute_all()
jobs             = data["jobs"]
talent           = data["talent"]
supply_df        = data["supply_df"]
exp_dist         = data["exp_dist"]
entry_skill_df   = data["entry_skill_df"]
talent_role_supply = data["talent_role_supply"]
role_demand      = data["role_demand"]
overlap_df       = data["overlap_df"]
overlap_by_role  = data["overlap_by_role"]
cat_skill_map    = data["cat_skill_map"]
work_type_dist   = data["work_type_dist"]
prov_dist        = data["prov_dist"]
salary_df        = data["salary_df"]
exp_skill_map    = data["exp_skill_map"]
total_talent     = data["total_talent"]
total_entry_cand = data["total_entry_cand"]

# ─── Helper: Metric Card ─────────────────────────────────────────────────────
def metric_card(label, value, delta=None, delta_label="", color=COLORS["primary"]):
    delta_html = ""
    if delta is not None:
        sign        = "▲" if delta >= 0 else "▼"
        delta_color = COLORS["accent"] if delta >= 0 else COLORS["danger"]
        delta_html  = f"<p style='color:{delta_color};font-size:0.78rem;margin:0'>{sign} {abs(delta):.1f}% {delta_label}</p>"
    st.markdown(
        f"""
        <div style='background:#fff;border-left:4px solid {color};border-radius:8px;
                    padding:0.9rem 1.1rem;margin-bottom:0.5rem;
                    box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
            <p style='color:#64748B;font-size:0.73rem;margin:0 0 3px 0;
                      text-transform:uppercase;letter-spacing:.06em;font-weight:600'>{label}</p>
            <p style='color:#1E293B;font-size:1.5rem;font-weight:800;margin:0'>{value}</p>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─── Helper: Section Header ──────────────────────────────────────────────────
def section_header(title, subtitle=""):
    sub = f"<p style='color:#64748B;font-size:0.85rem;margin:2px 0 0 0'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"<h4 style='color:#1E293B;margin:0 0 4px 0;font-size:1.05rem;font-weight:700'>{title}</h4>{sub}",
        unsafe_allow_html=True,
    )

# ─── Helper: Filter Box ──────────────────────────────────────────────────────
def filter_box():
    return st.container()

# ─── Helper: styled dataframe ────────────────────────────────────────────────
def show_df(df, height=None):
    """Render dataframe with stronger text styling."""
    kwargs = dict(use_container_width=True)
    if height:
        kwargs["height"] = height
    st.dataframe(df, **kwargs)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("BisaKerja · Tech Job Market Dashboard")
    st.markdown(
        "Analisis pasar kerja tech Indonesia — memetakan kebutuhan industri, "
        "profil kandidat, dan gap skill yang perlu dijembatani."
    )

    # ── Global Filters ────────────────────────────────────────────────────
    with st.expander("Filter Data", expanded=False):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            sel_cat = st.multiselect(
                "Kategori Pekerjaan",
                options=sorted(jobs["cat_group"].unique()),
                default=[],
                placeholder="Semua kategori",
            )
        with col_f2:
            sel_exp = st.multiselect(
                "Experience Level",
                options=["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"],
                default=[],
                placeholder="Semua level",
            )
        with col_f3:
            sel_wt = st.multiselect(
                "Work Type",
                options=sorted(jobs["work_type"].dropna().unique()),
                default=[],
                placeholder="Semua tipe",
            )

    jobs_f = jobs.copy()
    if sel_cat: jobs_f = jobs_f[jobs_f["cat_group"].isin(sel_cat)]
    if sel_exp: jobs_f = jobs_f[jobs_f["experience_level"].isin(sel_exp)]
    if sel_wt:  jobs_f = jobs_f[jobs_f["work_type"].isin(sel_wt)]

    st.divider()

    # ── KPI Row ───────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Total Lowongan Tech", f"{len(jobs_f):,}", color=COLORS["primary"])
    with c2:
        metric_card("Total Kandidat", f"{total_talent:,}", color=COLORS["secondary"])
    with c3:
        metric_card("Kandidat Entry-Level", f"{total_entry_cand:,}", color=COLORS["accent"])
    with c4:
        entry_n   = len(jobs_f[jobs_f["experience_level"] == "ENTRY_LEVEL"])
        entry_pct = round(entry_n / len(jobs_f) * 100, 1) if len(jobs_f) else 0
        metric_card("Lowongan Entry-Level", f"{entry_pct}%", color=COLORS["warning"])
    with c5:
        salary_pct = round(jobs_f["has_salary_info"].mean() * 100, 1) if len(jobs_f) else 0
        metric_card("Cantumkan Gaji", f"{salary_pct}%", color=COLORS["danger"])

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        section_header("Distribusi Experience Level Lowongan")
        exp_f = (
            jobs_f["experience_level"]
            .value_counts()
            .reindex(["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"], fill_value=0)
            .reset_index()
        )
        exp_f.columns = ["level", "count"]
        exp_f["pct"] = (exp_f["count"] / exp_f["count"].sum() * 100).round(1)
        fig = px.bar(
            exp_f, x="level", y="count",
            text=exp_f["pct"].apply(lambda x: f"{x}%"),
            color="count", color_continuous_scale=PALETTE_BLUE,
            labels={"level": "Level", "count": "Jumlah Lowongan"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(
            coloraxis_showscale=False, height=340,
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis_title=None, margin=dict(t=30, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        section_header("Kategori Pekerjaan Dominan")
        cat_grp = jobs_f["cat_group"].value_counts().reset_index()
        cat_grp.columns = ["Kategori", "Jumlah"]
        fig2 = px.bar(
            cat_grp.head(8).sort_values("Jumlah"),
            x="Jumlah", y="Kategori", orientation="h",
            color="Jumlah", color_continuous_scale=PALETTE_PURPLE, text="Jumlah",
        )
        fig2.update_traces(textposition="outside", marker_line_width=0)
        fig2.update_layout(
            coloraxis_showscale=False, height=340,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis_title=None, margin=dict(t=30, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Insight box ────────────────────────────────────────────────────────
    section_header("Insight Utama")
    cols = st.columns(3)
    with cols[0]:
        st.info(
            "**Entry-Level mendominasi** pasar dengan lebih dari 50% lowongan. "
            "Ini sinyal positif bagi lulusan baru masuk industri tech."
        )
    with cols[1]:
        st.info(
            "**IT & Software** adalah kategori terbesar, diikuti Data & Analytics "
            "dan QA & Testing. Diversifikasi karier tech masih terbuka lebar."
        )
    with cols[2]:
        st.info(
            f"**{total_talent:,} kandidat** tercatat dalam sistem dengan 7 role utama. "
            f"Hanya {salary_pct}% lowongan mencantumkan informasi gaji."
        )


# ════════════════════════════════════════════════════════════════════════════
# PAGE: SKILL DEMAND VS SUPPLY
# ════════════════════════════════════════════════════════════════════════════
elif page == "Skill: Demand vs Supply":
    st.title("Skill: Demand vs Supply")
    st.markdown(
        "Membandingkan skill paling banyak diminta lowongan tech Indonesia "
        "dengan persentase kandidat yang sudah memiliki skill tersebut."
    )

    # ── Filter ────────────────────────────────────────────────────────────
    with st.expander("Filter Tampilan", expanded=False):
        c1f, c2f = st.columns(2)
        with c1f:
            top_n_skill = st.slider("Tampilkan top N skill", min_value=5, max_value=20, value=10, step=1)
        with c2f:
            show_unmatched = st.checkbox("Tampilkan skill tanpa data kandidat", value=True)

    st.divider()
    matched   = supply_df[supply_df["matched"]].copy().head(top_n_skill)
    unmatched = supply_df[~supply_df["matched"]].copy()
    top_n_all = supply_df.head(top_n_skill)

    col1, col2 = st.columns([3, 2])
    with col1:
        section_header(f"Top {top_n_skill} Skill Paling Banyak Diminta (Lowongan)")
        fig = px.bar(
            top_n_all.sort_values("demand_count"),
            x="demand_count", y="skill", orientation="h",
            color="demand_count", color_continuous_scale=PALETTE_BLUE, text="demand_count",
            labels={"demand_count": "Jumlah Lowongan", "skill": "Skill"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(
            coloraxis_showscale=False, height=500,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis_title=None, margin=dict(t=10, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("% Kandidat yang Memiliki Skill", "Hanya skill yang terdata di kedua dataset")
        if not matched.empty:
            fig2 = px.bar(
                matched.sort_values("supply_pct"),
                x="supply_pct", y="skill", orientation="h",
                color="supply_pct", color_continuous_scale=PALETTE_TEAL,
                text=matched.sort_values("supply_pct")["supply_pct"].apply(lambda x: f"{x}%"),
                labels={"supply_pct": "% Kandidat", "skill": "Skill"},
            )
            fig2.update_traces(textposition="outside", marker_line_width=0)
            fig2.update_layout(
                coloraxis_showscale=False, height=350,
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis_title=None, margin=dict(t=10, b=10),
                font=dict(color="#1E293B"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        if show_unmatched and not unmatched.empty:
            section_header("Skill Diminta tapi Tidak Ada di Profil Kandidat")
            show_df(
                unmatched[["skill", "demand_count"]]
                .rename(columns={"skill": "Skill", "demand_count": "Jumlah Lowongan"})
                .reset_index(drop=True),
                height=200,
            )

    st.divider()
    section_header("Perbandingan Demand (Lowongan) vs Supply (Kandidat) per Skill")
    st.caption("Demand = jumlah lowongan. Supply = jumlah kandidat ÷ 100 (skala berbeda). Hanya skill yang ada di kedua dataset.")
    if not matched.empty:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="Demand (# Lowongan)", x=matched["skill"],
            y=matched["demand_count"], marker_color=COLORS["primary"],
        ))
        fig3.add_trace(go.Bar(
            name="Supply (# Kandidat / 100)", x=matched["skill"],
            y=matched["supply_count"] / 100, marker_color=COLORS["accent"],
        ))
        fig3.update_layout(
            barmode="group", height=380,
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_tickangle=-30, margin=dict(t=10, b=80),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.success("**Python** dan **SQL** adalah skill terpenting: keduanya masuk top demand dan dimiliki lebih dari 26% kandidat.")
    with c2:
        st.warning("**MySQL, PostgreSQL, Laravel, Go, Vue.js** banyak diminta industri tapi belum terdapat dalam profil kandidat — gap nyata yang perlu dijembatani.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: EXPERIENCE LEVEL
# ════════════════════════════════════════════════════════════════════════════
elif page == "Experience Level":
    st.title("Distribusi Experience Level")
    st.markdown(
        "Memetakan struktur kebutuhan tenaga kerja berdasarkan senioritas, "
        "dan mengevaluasi kesiapan kandidat awal karier terhadap posisi entry-level."
    )

    # ── Filter ────────────────────────────────────────────────────────────
    with st.expander("Filter Tampilan", expanded=False):
        cf1, cf2 = st.columns(2)
        with cf1:
            sel_wt_exp = st.multiselect(
                "Work Type",
                options=sorted(jobs["work_type"].dropna().unique()),
                default=[], placeholder="Semua tipe",
            )
        with cf2:
            sel_cat_exp = st.multiselect(
                "Kategori",
                options=sorted(jobs["cat_group"].unique()),
                default=[], placeholder="Semua kategori",
            )

    jobs_fe = jobs.copy()
    if sel_wt_exp:  jobs_fe = jobs_fe[jobs_fe["work_type"].isin(sel_wt_exp)]
    if sel_cat_exp: jobs_fe = jobs_fe[jobs_fe["cat_group"].isin(sel_cat_exp)]

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        section_header("Distribusi Experience Level Lowongan")
        exp_f = (
            jobs_fe["experience_level"].value_counts()
            .reindex(["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"], fill_value=0)
            .reset_index()
        )
        exp_f.columns = ["level", "count"]
        exp_f["pct"] = (exp_f["count"] / exp_f["count"].sum() * 100).round(1)

        fig = px.pie(
            exp_f, names="level", values="count",
            hole=0.45, color_discrete_sequence=PALETTE_CAT,
        )
        fig.update_traces(textinfo="label+percent", textposition="outside",
                          textfont=dict(color="#1E293B", size=12))
        fig.update_layout(height=380, margin=dict(t=20, b=20),
                          font=dict(color="#1E293B"))
        st.plotly_chart(fig, use_container_width=True)

        show_df(
            exp_f.rename(columns={"level": "Level", "count": "Lowongan", "pct": "%"})
            .set_index("Level")
        )

    with col2:
        section_header("Top Skill per Experience Level")
        level_filter = st.selectbox(
            "Pilih experience level:",
            ["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"],
        )
        skill_data = exp_skill_map[level_filter]
        if skill_data:
            df_tmp = pd.DataFrame(skill_data)
            fig2 = px.bar(
                df_tmp.sort_values("count"),
                x="count", y="skill", orientation="h",
                color="count", color_continuous_scale=PALETTE_PURPLE, text="count",
                labels={"count": "# Lowongan", "skill": "Skill"},
            )
            fig2.update_traces(textposition="outside", marker_line_width=0)
            fig2.update_layout(
                coloraxis_showscale=False, height=380,
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis_title=None, margin=dict(t=10, b=10),
                font=dict(color="#1E293B"),
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    section_header(
        f"Kesiapan Kandidat Entry-Level (Fresher & 1-2 Tahun)",
        f"Berdasarkan {total_entry_cand:,} kandidat entry-level vs top skill yang diminta lowongan ENTRY_LEVEL"
    )
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        name="Diminta Lowongan (# jobs)",
        x=entry_skill_df["skill"], y=entry_skill_df["entry_job_count"],
        marker_color=COLORS["primary"],
    ))
    fig3.add_trace(go.Bar(
        name="Kandidat Memiliki (%)",
        x=entry_skill_df["skill"], y=entry_skill_df["candidate_pct"],
        marker_color=COLORS["accent"], yaxis="y2",
    ))
    fig3.update_layout(
        barmode="group", height=380,
        yaxis=dict(title="# Lowongan yang Minta", side="left", color="#1E293B"),
        yaxis2=dict(title="% Kandidat Punya Skill", side="right", overlaying="y", color="#1E293B"),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_tickangle=-30, margin=dict(t=10, b=80),
        font=dict(color="#1E293B"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    section_header("Distribusi Experience Kandidat")
    talent_exp = talent["Experience"].value_counts().reset_index()
    talent_exp.columns = ["Experience", "Jumlah"]
    fig4 = px.bar(
        talent_exp, x="Experience", y="Jumlah",
        color="Experience", color_discrete_sequence=PALETTE_CAT, text="Jumlah",
    )
    fig4.update_traces(textposition="outside", showlegend=False)
    fig4.update_layout(
        height=300, plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title=None, margin=dict(t=10, b=10),
        font=dict(color="#1E293B"),
    )
    st.plotly_chart(fig4, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.info("**ENTRY_LEVEL** mendominasi 52% lowongan — pasar sangat terbuka untuk fresh graduate dan kandidat berpengalaman < 1 tahun.")
    with c2:
        st.info("Kandidat fresher dan 1-2 tahun menguasai **Python, React, Git, SQL** — skill relevan dengan kebutuhan entry-level. Gap utama ada di MySQL, PostgreSQL, dan framework backend spesifik.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: JOB ROLE & KANDIDAT
# ════════════════════════════════════════════════════════════════════════════
elif page == "Job Role & Kandidat":
    st.title("Job Role & Proporsi Kandidat")
    st.markdown(
        "Melihat role tech paling banyak tersedia di pasar kerja dan membandingkan "
        "dengan proporsi kandidat yang sesuai."
    )

    # ── Filter ────────────────────────────────────────────────────────────
    with st.expander("Filter Tampilan", expanded=False):
        cf1, cf2 = st.columns(2)
        with cf1:
            top_n_role = st.slider("Top N role lowongan", 5, 15, 10)
        with cf2:
            sel_role_cand = st.multiselect(
                "Filter role kandidat",
                options=sorted(talent["Job_Role"].dropna().unique()),
                default=[], placeholder="Semua role",
            )

    talent_f = talent.copy()
    if sel_role_cand:
        talent_f = talent_f[talent_f["Job_Role"].isin(sel_role_cand)]
    role_demand_f = data["role_demand"].head(top_n_role)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        section_header("Top Job Roles di Lowongan")
        fig = px.bar(
            role_demand_f.sort_values("demand"),
            x="demand", y="role", orientation="h",
            color="demand", color_continuous_scale=PALETTE_BLUE, text="demand",
            labels={"demand": "Jumlah Lowongan", "role": "Role"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(
            coloraxis_showscale=False, height=440,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis_title=None, margin=dict(t=10, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Distribusi Kandidat berdasarkan Job Role")
        role_supply_f = talent_f["Job_Role"].value_counts().reset_index()
        role_supply_f.columns = ["role", "supply_count"]
        role_supply_f["supply_pct"] = (role_supply_f["supply_count"] / len(talent_f) * 100).round(1)

        fig2 = px.pie(
            role_supply_f, names="role", values="supply_count",
            hole=0.4, color_discrete_sequence=PALETTE_CAT,
        )
        fig2.update_traces(textinfo="label+percent", textposition="outside",
                           textfont=dict(color="#1E293B", size=11))
        fig2.update_layout(height=300, margin=dict(t=20, b=20),
                           font=dict(color="#1E293B"))
        st.plotly_chart(fig2, use_container_width=True)

        show_df(
            role_supply_f.rename(
                columns={"role": "Role", "supply_count": "Kandidat", "supply_pct": "%"}
            ).set_index("Role"),
            height=220,
        )

    st.divider()
    section_header("Demand (Lowongan) vs Supply Kandidat per Role")
    st.caption("Supply kandidat dihitung dari seluruh kandidat dengan role tersebut ÷ 100.")

    role_merged = role_demand_f.merge(
        role_supply_f[["role", "supply_count"]], on="role", how="left"
    ).fillna(0)

    if not role_merged.empty:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="Demand (# Lowongan)", x=role_merged["role"],
            y=role_merged["demand"], marker_color=COLORS["primary"],
        ))
        fig3.add_trace(go.Bar(
            name="Supply Kandidat (/100)", x=role_merged["role"],
            y=role_merged["supply_count"] / 100, marker_color=COLORS["secondary"],
        ))
        fig3.update_layout(
            barmode="group", height=380,
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_tickangle=-35, margin=dict(t=10, b=100),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.info("Dari sisi lowongan, **IT Support**, **Software Engineer**, dan role backend masih mendominasi pasar lowongan kerja tech Indonesia.")
    with c2:
        st.info("Distribusi kandidat relatif merata di 7 role utama (Cloud, Data Scientist, Cybersecurity, Web Dev, BA, Backend, ML). Ini bisa mengindikasikan oversupply di beberapa role.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: SKILL OVERLAP
# ════════════════════════════════════════════════════════════════════════════
elif page == "Skill Overlap":
    st.title("Skill Overlap: Kandidat vs Lowongan Entry-Level")
    st.markdown(
        "Mengukur seberapa besar kemiripan skill kandidat entry-level dengan "
        "persyaratan skill lowongan entry-level, dibreakdown per role dan experience."
    )

    # ── Filter ────────────────────────────────────────────────────────────
    with st.expander("Filter Tampilan", expanded=False):
        cf1, cf2 = st.columns(2)
        with cf1:
            sel_role_ov = st.multiselect(
                "Filter Role Kandidat",
                options=sorted(overlap_df["role"].unique()),
                default=[], placeholder="Semua role",
            )
        with cf2:
            sel_exp_ov = st.multiselect(
                "Filter Experience",
                options=sorted(overlap_df["experience"].unique()),
                default=[], placeholder="Semua",
            )

    ov_f = overlap_df.copy()
    if sel_role_ov: ov_f = ov_f[ov_f["role"].isin(sel_role_ov)]
    if sel_exp_ov:  ov_f = ov_f[ov_f["experience"].isin(sel_exp_ov)]

    avg_overlap = ov_f["overlap_pct"].mean()
    med_overlap = ov_f["overlap_pct"].median()

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Rata-rata Skill Overlap", f"{avg_overlap:.1f}%", color=COLORS["primary"])
    with c2:
        metric_card("Median Skill Overlap", f"{med_overlap:.1f}%", color=COLORS["secondary"])
    with c3:
        metric_card("Kandidat Entry-Level", f"{len(ov_f):,}", color=COLORS["accent"])
    with c4:
        high_overlap = (ov_f["overlap_pct"] >= 50).sum()
        metric_card("Overlap >= 50%", f"{high_overlap:,}", color=COLORS["warning"])

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        section_header("Rata-rata Skill Overlap per Role Kandidat")
        ov_by_role_f = (
            ov_f.groupby("role")["overlap_pct"]
            .agg(["mean", "median", "count"]).reset_index()
        )
        ov_by_role_f.columns = ["role", "mean_overlap", "median_overlap", "candidate_count"]
        ov_by_role_f["mean_overlap"] = ov_by_role_f["mean_overlap"].round(1)
        ov_by_role_f = ov_by_role_f.sort_values("mean_overlap")

        fig = px.bar(
            ov_by_role_f,
            x="mean_overlap", y="role", orientation="h",
            color="mean_overlap", color_continuous_scale="RdYlGn",
            text=ov_by_role_f["mean_overlap"].apply(lambda x: f"{x:.1f}%"),
            labels={"mean_overlap": "Rata-rata Overlap (%)", "role": "Role"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(
            coloraxis_showscale=False, height=360,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis_title=None, margin=dict(t=10, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Distribusi Skill Overlap (Histogram)")
        fig2 = px.histogram(
            ov_f, x="overlap_pct", nbins=20,
            color_discrete_sequence=[COLORS["primary"]],
            labels={"overlap_pct": "Skill Overlap (%)"},
        )
        fig2.add_vline(
            x=avg_overlap, line_dash="dash", line_color=COLORS["danger"],
            annotation_text=f"Rata-rata: {avg_overlap:.1f}%",
            annotation_position="top right",
        )
        fig2.update_layout(
            height=270, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(t=10, b=10), bargap=0.05,
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig2, use_container_width=True)

        section_header("Detail per Role")
        show_df(
            ov_by_role_f.sort_values("mean_overlap", ascending=False)
            .rename(columns={
                "role": "Role", "mean_overlap": "Avg Overlap (%)",
                "median_overlap": "Median (%)", "candidate_count": "# Kandidat",
            }).set_index("Role"),
            height=200,
        )

    st.divider()
    section_header("Skill Overlap berdasarkan Experience Kandidat")
    ov_exp = (
        ov_f.groupby("experience")["overlap_pct"]
        .agg(["mean", "median", "count"]).reset_index()
    )
    ov_exp.columns = ["experience", "mean_overlap", "median_overlap", "count"]
    ov_exp["mean_overlap"] = ov_exp["mean_overlap"].round(1)

    fig3 = px.bar(
        ov_exp, x="experience", y="mean_overlap",
        color="mean_overlap", color_continuous_scale="RdYlGn",
        text=ov_exp["mean_overlap"].apply(lambda x: f"{x:.1f}%"),
        labels={"mean_overlap": "Rata-rata Overlap (%)", "experience": "Experience"},
    )
    fig3.update_traces(textposition="outside")
    fig3.update_layout(
        coloraxis_showscale=False, height=280,
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title=None, margin=dict(t=10, b=10),
        font=dict(color="#1E293B"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    if not ov_by_role_f.empty:
        best  = ov_by_role_f.iloc[-1]
        worst = ov_by_role_f.iloc[0]
        c1, c2 = st.columns(2)
        with c1:
            st.success(f"**{best['role']}** memiliki overlap tertinggi ({best['mean_overlap']:.1f}%), menunjukkan kandidat di role ini paling siap untuk posisi entry-level.")
        with c2:
            st.warning(f"**{worst['role']}** memiliki overlap terendah ({worst['mean_overlap']:.1f}%), menandakan gap skill signifikan dan peluang upskilling terbesar.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: SKILL PER KATEGORI
# ════════════════════════════════════════════════════════════════════════════
elif page == "Skill per Kategori":
    st.title("Skill per Kategori Pekerjaan")
    st.markdown(
        "Menampilkan skill yang paling sering diminta di setiap kategori pekerjaan, "
        "membantu kandidat fokus pada skill paling relevan untuk kategori yang dituju."
    )

    # ── Filter ────────────────────────────────────────────────────────────
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        selected_cat = st.selectbox(
            "Pilih Kategori:",
            sorted(cat_skill_map.keys()),
        )
    with col_f2:
        top_n_cat = st.slider("Top N skill", 5, 20, 12)

    st.divider()

    cat_counter = cat_skill_map[selected_cat]
    df_cat = pd.DataFrame(cat_counter.most_common(top_n_cat), columns=["Skill", "Jumlah Lowongan"])

    col1, col2 = st.columns([2, 1])
    with col1:
        section_header(f"Top {top_n_cat} Skill — {selected_cat}")
        fig = px.bar(
            df_cat.sort_values("Jumlah Lowongan"),
            x="Jumlah Lowongan", y="Skill", orientation="h",
            color="Jumlah Lowongan", color_continuous_scale=PALETTE_BLUE, text="Jumlah Lowongan",
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(
            coloraxis_showscale=False, height=max(380, top_n_cat * 32),
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis_title=None, margin=dict(t=10, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Tabel Detail")
        show_df(df_cat.reset_index(drop=True), height=max(380, top_n_cat * 32))

    st.divider()

    # ── Heatmap lintas kategori ────────────────────────────────────────────
    section_header("Heatmap Skill Lintas Kategori", "Persentase kemunculan skill di setiap kategori (top 12 skill global)")

    hm_top_n = st.slider("Jumlah skill global untuk heatmap", 6, 15, 12, key="hm_slider")
    global_top   = data["job_skill_counter"].most_common(hm_top_n)
    top_skills_g = [s for s, _ in global_top]

    heat_data = {}
    for cat in sorted(cat_skill_map.keys()):
        cc    = cat_skill_map[cat]
        total = sum(cc.values()) or 1
        heat_data[cat] = {sk: cc.get(sk, 0) / total * 100 for sk in top_skills_g}
    heat_df = pd.DataFrame(heat_data, index=top_skills_g).T

    fig2 = px.imshow(
        heat_df, color_continuous_scale="Blues",
        aspect="auto", text_auto=".1f",
        labels=dict(color="% dalam Kategori"),
    )
    fig2.update_layout(
        height=420, margin=dict(t=10, b=10),
        font=dict(color="#1E293B"),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.info("**SQL, Python, dan CI/CD** adalah skill lintas kategori yang paling konsisten dibutuhkan. Kandidat yang menguasai ketiganya memiliki fleksibilitas terluas di pasar tech Indonesia.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: LOKASI & WORK TYPE
# ════════════════════════════════════════════════════════════════════════════
elif page == "Lokasi & Work Type":
    st.title("Lokasi & Work Type")
    st.markdown(
        "Distribusi geografis lowongan tech Indonesia dan preferensi pola kerja "
        "(onsite, hybrid, remote) di pasar saat ini."
    )

    # ── Filter ────────────────────────────────────────────────────────────
    with st.expander("Filter Tampilan", expanded=False):
        cf1, cf2, cf3 = st.columns(3)
        with cf1:
            sel_exp_loc = st.multiselect(
                "Experience Level",
                options=["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"],
                default=[], placeholder="Semua level",
            )
        with cf2:
            sel_cat_loc = st.multiselect(
                "Kategori",
                options=sorted(jobs["cat_group"].unique()),
                default=[], placeholder="Semua kategori",
            )
        with cf3:
            top_n_prov = st.slider("Top N provinsi", 5, 15, 12)

    jobs_fl = jobs.copy()
    if sel_exp_loc: jobs_fl = jobs_fl[jobs_fl["experience_level"].isin(sel_exp_loc)]
    if sel_cat_loc: jobs_fl = jobs_fl[jobs_fl["cat_group"].isin(sel_cat_loc)]

    prov_f = jobs_fl["province_norm"].value_counts().head(top_n_prov).reset_index()
    prov_f.columns = ["province", "count"]
    wt_f = jobs_fl["work_type"].value_counts().reset_index()
    wt_f.columns = ["work_type", "count"]
    wt_f["pct"] = (wt_f["count"] / wt_f["count"].sum() * 100).round(1)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        section_header(f"Top {top_n_prov} Provinsi / Wilayah Lowongan")
        fig = px.bar(
            prov_f.sort_values("count"),
            x="count", y="province", orientation="h",
            color="count", color_continuous_scale=PALETTE_BLUE, text="count",
            labels={"count": "Jumlah Lowongan", "province": "Provinsi"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(
            coloraxis_showscale=False, height=420,
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis_title=None, margin=dict(t=10, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Distribusi Work Type")
        fig2 = px.pie(
            wt_f, names="work_type", values="count", hole=0.45,
            color_discrete_sequence=[COLORS["primary"], COLORS["accent"], COLORS["secondary"]],
        )
        fig2.update_traces(
            textinfo="label+percent+value", textposition="outside",
            textfont=dict(color="#1E293B", size=11),
        )
        fig2.update_layout(height=300, margin=dict(t=20, b=20),
                           font=dict(color="#1E293B"))
        st.plotly_chart(fig2, use_container_width=True)

        show_df(
            wt_f.rename(columns={"work_type": "Work Type", "count": "Lowongan", "pct": "%"})
            .set_index("Work Type")
        )

    st.divider()

    section_header("Work Type per Experience Level")
    wt_exp = (
        jobs_fl.groupby(["experience_level", "work_type"]).size().reset_index(name="count")
    )
    exp_order_list = ["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"]
    wt_exp["experience_level"] = pd.Categorical(
        wt_exp["experience_level"], categories=exp_order_list, ordered=True
    )
    wt_exp = wt_exp.sort_values("experience_level")

    fig3 = px.bar(
        wt_exp, x="experience_level", y="count", color="work_type",
        barmode="group",
        color_discrete_sequence=[COLORS["primary"], COLORS["accent"], COLORS["secondary"]],
        labels={"experience_level": "Level", "count": "Jumlah Lowongan", "work_type": "Work Type"},
    )
    fig3.update_layout(
        height=340, plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=None, margin=dict(t=10, b=10),
        font=dict(color="#1E293B"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    c1, c2 = st.columns(2)
    onsite_pct = wt_f[wt_f["work_type"] == "ONSITE"]["pct"].values
    onsite_pct = onsite_pct[0] if len(onsite_pct) > 0 else 0
    with c1:
        st.info(f"**{onsite_pct:.0f}% lowongan bersifat ONSITE** — pasar tech Indonesia masih sangat dominan meminta kehadiran fisik, terutama untuk entry dan junior level.")
    with c2:
        st.info("**DKI Jakarta** menjadi episentrum lowongan tech Indonesia, diikuti Jawa Barat dan Banten. Konsentrasi tinggi di Jabodetabek perlu diperhatikan oleh kandidat di luar Jawa.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: ANALISIS GAJI
# ════════════════════════════════════════════════════════════════════════════
elif page == "Analisis Gaji":
    st.title("Analisis Gaji Lowongan Tech")
    st.markdown(
        "Gambaran kompensasi di pasar kerja tech Indonesia, "
        "khususnya untuk lowongan yang mencantumkan informasi gaji."
    )

    # ── Filter ────────────────────────────────────────────────────────────
    with st.expander("Filter Tampilan", expanded=False):
        cf1, cf2, cf3 = st.columns(3)
        with cf1:
            sel_exp_sal = st.multiselect(
                "Experience Level",
                options=["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"],
                default=[], placeholder="Semua level",
            )
        with cf2:
            sel_cat_sal = st.multiselect(
                "Kategori",
                options=sorted(salary_df["cat_group"].unique()),
                default=[], placeholder="Semua kategori",
            )
        with cf3:
            sal_max = st.slider("Gaji max (juta Rp)", 5, 100, 30)

    sal_f = salary_df.copy()
    if sel_exp_sal: sal_f = sal_f[sal_f["experience_level"].isin(sel_exp_sal)]
    if sel_cat_sal: sal_f = sal_f[sal_f["cat_group"].isin(sel_cat_sal)]
    sal_f = sal_f[sal_f["salary_min_m"] <= sal_max]

    has_sal    = len(sal_f)
    no_sal     = len(jobs) - len(salary_df)
    median_sal = sal_f["salary_min_m"].median() if len(sal_f) else 0
    avg_sal    = sal_f["salary_min_m"].mean() if len(sal_f) else 0

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Lowongan dengan Gaji", f"{has_sal:,}", color=COLORS["primary"])
    with c2:
        metric_card("Tanpa Info Gaji", f"{no_sal:,}", color=COLORS["danger"])
    with c3:
        metric_card("Median Gaji Min", f"Rp {median_sal:.1f} Jt", color=COLORS["accent"])
    with c4:
        metric_card("Rata-rata Gaji Min", f"Rp {avg_sal:.1f} Jt", color=COLORS["warning"])

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        section_header("Distribusi Gaji Minimum (Juta Rupiah)")
        fig = px.histogram(
            sal_f, x="salary_min_m", nbins=25,
            color_discrete_sequence=[COLORS["primary"]],
            labels={"salary_min_m": "Gaji Minimum (Juta Rp)"},
        )
        if median_sal > 0:
            fig.add_vline(
                x=median_sal, line_dash="dash", line_color=COLORS["danger"],
                annotation_text=f"Median: Rp {median_sal:.1f} Jt",
                annotation_position="top right",
            )
        fig.update_layout(
            height=300, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(t=10, b=10), bargap=0.05,
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("Median Gaji per Experience Level")
        sal_exp = (
            sal_f.groupby("experience_level")["salary_min_m"]
            .median()
            .reindex(["ENTRY_LEVEL", "JUNIOR", "MID_LEVEL", "SENIOR", "LEAD"])
            .reset_index().dropna()
        )
        sal_exp.columns = ["Level", "Median Gaji Min (Jt)"]
        fig2 = px.bar(
            sal_exp, x="Level", y="Median Gaji Min (Jt)",
            color="Median Gaji Min (Jt)", color_continuous_scale=PALETTE_TEAL,
            text=sal_exp["Median Gaji Min (Jt)"].apply(lambda x: f"Rp {x:.1f} Jt"),
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(
            coloraxis_showscale=False, height=300,
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis_title=None, margin=dict(t=10, b=10),
            font=dict(color="#1E293B"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    section_header("Median Gaji per Kategori Pekerjaan")
    sal_cat = (
        sal_f.groupby("cat_group")["salary_min_m"]
        .median().sort_values(ascending=False).reset_index()
    )
    sal_cat.columns = ["Kategori", "Median Gaji Min (Jt)"]

    fig3 = px.bar(
        sal_cat.sort_values("Median Gaji Min (Jt)"),
        x="Median Gaji Min (Jt)", y="Kategori", orientation="h",
        color="Median Gaji Min (Jt)", color_continuous_scale=PALETTE_PURPLE,
        text=sal_cat.sort_values("Median Gaji Min (Jt)")["Median Gaji Min (Jt)"].apply(
            lambda x: f"Rp {x:.1f} Jt"
        ),
    )
    fig3.update_traces(textposition="outside")
    fig3.update_layout(
        coloraxis_showscale=False, height=340,
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis_title=None, margin=dict(t=10, b=10),
        font=dict(color="#1E293B"),
    )
    st.plotly_chart(fig3, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"Median gaji minimum tech di Indonesia sekitar **Rp {median_sal:.0f} juta/bulan**, dengan semakin tinggi level semakin besar kompensasi yang ditawarkan.")
    with c2:
        st.warning(f"Hanya **{round(len(salary_df)/len(jobs)*100):.0f}% lowongan** mencantumkan gaji — transparansi kompensasi masih menjadi tantangan di pasar kerja tech Indonesia.")


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#94A3B8;font-size:0.78rem;padding:0.8rem'>"
    "BisaKerja Dashboard &nbsp;·&nbsp; Capstone Project CC26-PSU263 &nbsp;·&nbsp; Coding Camp 2026 by DBS Foundation"
    "</div>",
    unsafe_allow_html=True,
)
