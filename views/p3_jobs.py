"""
💼 Project 3: Job Market Analytics Platform — Live Demo
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
import random
from collections import Counter

# ── Currency constants ──
INR_RATE = 84  # 1 USD = 84 INR


# ── Skill Taxonomy (subset from the real project) ──
SKILL_TAXONOMY = {
    "Programming": {
        "Python": [r"\bpython\b"], "SQL": [r"\bsql\b"], "Java": [r"\bjava\b(?!script)"],
        "Scala": [r"\bscala\b"], "R": [r"\bR\b"], "Go": [r"\bgo\b", r"\bgolang\b"],
        "JavaScript": [r"\bjavascript\b", r"\bnode\.?js\b"],
    },
    "Data Engineering": {
        "Apache Spark": [r"\bspark\b", r"\bpyspark\b"], "Kafka": [r"\bkafka\b"],
        "Airflow": [r"\bairflow\b"], "dbt": [r"\bdbt\b"],
        "Data Pipeline": [r"\bpipeline\b", r"\betl\b", r"\belt\b"],
        "Data Lake": [r"\bdata lake\b", r"\blakehouse\b"],
    },
    "Cloud & DevOps": {
        "AWS": [r"\baws\b", r"\bs3\b", r"\bredshift\b", r"\bglue\b"],
        "GCP": [r"\bgcp\b", r"\bbigquery\b", r"\bdataflow\b"],
        "Azure": [r"\bazure\b", r"\bsynapse\b"],
        "Docker": [r"\bdocker\b"], "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
        "CI/CD": [r"\bci/?cd\b", r"\bgithub\s*actions\b"],
    },
    "Databases": {
        "PostgreSQL": [r"\bpostgres\b", r"\bpostgresql\b"],
        "MongoDB": [r"\bmongodb\b", r"\bmongo\b"], "Redis": [r"\bredis\b"],
        "Snowflake": [r"\bsnowflake\b"], "Databricks": [r"\bdatabricks\b"],
    },
}

SAMPLE_JOB_DESCRIPTIONS = [
    """Senior Data Engineer — TechCorp
We are looking for a Senior Data Engineer with 3+ years of experience in Python and SQL.
You will build and maintain ETL pipelines using Apache Spark and Airflow.
Experience with AWS (S3, Redshift, Glue) and dbt is required.
Nice to have: Kafka, Docker, Kubernetes, CI/CD.
Salary: $140,000 - $180,000 USD""",

    """Data Engineer — Analytics Startup
Join our fast-growing team! We need someone skilled in Python, SQL, and PostgreSQL.
Build data pipelines with Airflow and dbt. Experience with GCP (BigQuery, Dataflow)
is a plus. Must know Docker and have passion for data lake architectures.
Salary: £65,000 - £85,000 GBP""",

    """Staff Data Engineer — FinTech
Lead our data platform migration to Snowflake & Databricks. Deep expertise in
Spark, Scala, and Kafka required. Must have 5+ years building production data
pipelines. Experience with Kubernetes, CI/CD, and data lake patterns.
Salary: €90,000 - €120,000 EUR""",
]


def extract_skills(text: str) -> dict:
    """Extract skills from job description using regex taxonomy."""
    results = {}
    for category, skills in SKILL_TAXONOMY.items():
        found = []
        for skill_name, patterns in skills.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    found.append(skill_name)
                    break
        if found:
            results[category] = found
    return results


def normalize_salary(text: str) -> dict:
    """Extract and normalize salary to USD."""
    fx_rates = {"USD": 1.0, "GBP": 1.27, "EUR": 1.09, "INR": 0.012, "CAD": 0.74}

    patterns = [
        r'\$\s*([\d,]+)\s*[-–to]+\s*\$?\s*([\d,]+)',
        r'£\s*([\d,]+)\s*[-–to]+\s*£?\s*([\d,]+)',
        r'€\s*([\d,]+)\s*[-–to]+\s*€?\s*([\d,]+)',
    ]
    symbols = {"$": "USD", "£": "GBP", "€": "EUR"}

    for sym, currency in symbols.items():
        for pat in patterns:
            if sym in pat or True:
                match = re.search(pat.replace("$", re.escape(sym)) if sym != "$" else pat, text)
                if match:
                    low = int(match.group(1).replace(",", ""))
                    high = int(match.group(2).replace(",", ""))
                    rate = fx_rates.get(currency, 1.0)
                    return {
                        "currency": currency, "min_local": low, "max_local": high,
                        "min_usd": int(low * rate), "max_usd": int(high * rate),
                        "mid_usd": int((low + high) / 2 * rate),
                    }
    return None


def render():
    st.markdown("""
    <div class="hero-container" style="background: linear-gradient(135deg, #1a1f2e 0%, #4a3f00 50%, #1a1f2e 100%);">
        <div class="hero-title" style="font-size:2rem;">💼 Job Market Analytics</div>
        <div class="hero-subtitle">NLP Skill Extraction → Salary Normalization → Market Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📐 Architecture", expanded=False):
        st.markdown("""
        ```
        Job Postings ──→ NLP Skill Extractor (100+ regex patterns)
                              │
                    ┌─────────┼──────────┐
                 Skills    Salary      Location
                    │         │           │
              Taxonomy    FX Norm     Geocoding
                    │         │           │
                    └─────────┴──────────┘
                              │
                        PostgreSQL → dbt Star Schema
                              │
                   fct_job_skills + dim_skills + dim_companies
        ```
        **Tech:** Regex NLP, Multi-Currency FX, PostgreSQL, dbt, Airflow
        """)

    st.markdown("### 📝 Paste a Job Description")
    tab1, tab2 = st.tabs(["📋 Use Sample", "✏️ Custom Input"])

    with tab1:
        sample_idx = st.selectbox("Select sample:", range(len(SAMPLE_JOB_DESCRIPTIONS)),
                                 format_func=lambda i: f"Sample {i+1}: {SAMPLE_JOB_DESCRIPTIONS[i].split(chr(10))[0]}")
        jd_text = SAMPLE_JOB_DESCRIPTIONS[sample_idx]
        st.text_area("Job Description:", jd_text, height=200, disabled=True, key="sample_jd")

    with tab2:
        jd_text_custom = st.text_area(
            "Paste any job description here:",
            placeholder="Senior Data Engineer...\nRequired: Python, Spark, Airflow...\nSalary: $120,000 - $150,000",
            height=200, key="custom_jd",
        )
        if jd_text_custom:
            jd_text = jd_text_custom

    if st.button("🔍 Extract Skills & Analyze", use_container_width=True, type="primary"):
        skills = extract_skills(jd_text)
        salary = normalize_salary(jd_text)

        if not skills:
            st.warning("No recognized skills found. Try a more detailed job description.")
            return

        # ── Metrics ──
        cur = st.session_state.get("currency", "USD")
        sym = "\u20b9" if cur == "INR" else "$"
        total_skills = sum(len(v) for v in skills.values())
        m1, m2, m3 = st.columns(3)
        m1.metric("Skills Extracted", total_skills)
        m2.metric("Categories", len(skills))
        if salary:
            mid = salary['mid_usd']
            display_val = f"{sym}{int(mid * INR_RATE):,}" if cur == "INR" else f"${mid:,}"
            m3.metric(f"Salary ({cur})", display_val)
        else:
            m3.metric("Salary", "Not found")

        # ── Skill Breakdown ──
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 🏷️ Extracted Skills")
            for cat, skill_list in skills.items():
                badges = " ".join(f'`{s}`' for s in skill_list)
                st.markdown(f"**{cat}:** {badges}")

        with col2:
            # Skill category pie chart
            cat_data = pd.DataFrame([
                {"category": cat, "count": len(sk)} for cat, sk in skills.items()
            ])
            fig = px.pie(cat_data, names="category", values="count",
                        title="📊 Skills by Category",
                        color_discrete_sequence=["#6C63FF", "#FF6B6B", "#4ECDC4", "#FFD93D", "#00D4FF"])
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig, use_container_width=True)

        # ── Salary Normalization ──
        if salary:
            st.markdown("#### 💰 Salary Normalization")
            sal_col1, sal_col2 = st.columns(2)
            with sal_col1:
                if cur == "INR":
                    min_disp = int(salary['min_usd'] * INR_RATE)
                    max_disp = int(salary['max_usd'] * INR_RATE)
                    mid_disp = int(salary['mid_usd'] * INR_RATE)
                    st.markdown(f"""
                    | Field | Value |
                    |-------|-------|
                    | Original Currency | **{salary['currency']}** |
                    | Local Range | {salary['min_local']:,} — {salary['max_local']:,} |
                    | INR Range | **\u20b9{min_disp:,} — \u20b9{max_disp:,}** |
                    | INR Midpoint | **\u20b9{mid_disp:,}** |
                    """)
                else:
                    st.markdown(f"""
                    | Field | Value |
                    |-------|-------|
                    | Original Currency | **{salary['currency']}** |
                    | Local Range | {salary['min_local']:,} — {salary['max_local']:,} |
                    | USD Range | **${salary['min_usd']:,} — ${salary['max_usd']:,}** |
                    | USD Midpoint | **${salary['mid_usd']:,}** |
                    """)
            with sal_col2:
                if cur == "INR":
                    yvals = [int(salary['min_usd'] * INR_RATE),
                             int(salary['mid_usd'] * INR_RATE),
                             int(salary['max_usd'] * INR_RATE)]
                    bar_labels = [f"\u20b9{v:,}" for v in yvals]
                    bar_title = "Normalized Salary (INR)"
                    x_labels = ["Min INR", "Midpoint", "Max INR"]
                else:
                    yvals = [salary['min_usd'], salary['mid_usd'], salary['max_usd']]
                    bar_labels = [f"${v:,}" for v in yvals]
                    bar_title = "Normalized Salary (USD)"
                    x_labels = ["Min USD", "Midpoint", "Max USD"]

                fig2 = go.Figure(go.Bar(
                    x=x_labels,
                    y=yvals,
                    marker_color=["#4ECDC4", "#6C63FF", "#FF6B6B"],
                    text=bar_labels,
                    textposition="auto",
                ))
                fig2.update_layout(title=bar_title, template="plotly_dark",
                                 paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=250)
                st.plotly_chart(fig2, use_container_width=True)

        # ── Market Demand Simulation ──
        st.markdown("#### 📈 Simulated Market Demand (Top Skills)")
        all_skills = [s for sl in skills.values() for s in sl]
        demand_data = pd.DataFrame({
            "skill": all_skills,
            "job_count": [random.randint(200, 5000) for _ in all_skills],
            "avg_salary_usd": [random.randint(80000, 200000) for _ in all_skills],
        })
        if cur == "INR":
            demand_data["avg_salary_inr"] = (demand_data["avg_salary_usd"] * INR_RATE).astype(int)
            color_col = "avg_salary_inr"
            color_label = "Avg Salary (\u20b9)"
        else:
            color_col = "avg_salary_usd"
            color_label = "Avg Salary ($)"
        demand_data = demand_data.sort_values("job_count", ascending=True)

        fig3 = px.bar(demand_data, x="job_count", y="skill", orientation="h",
                     color=color_col, color_continuous_scale="Viridis",
                     title=f"Market Demand vs. Salary ({cur})",
                     labels={color_col: color_label})
        fig3.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                         plot_bgcolor="rgba(0,0,0,0)", height=max(250, len(all_skills) * 35))
        st.plotly_chart(fig3, use_container_width=True)
