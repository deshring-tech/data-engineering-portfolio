"""
🏠 Home Page — Resume & Portfolio Overview
"""
import streamlit as st


def render():
    # ── Hero Section ──
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Data Engineering Portfolio</div>
        <div class="hero-subtitle">
            5 Production-Grade Projects · 150+ Files · End-to-End Pipelines
        </div>
        <div style="margin-top:1rem;">
            <span class="skill-badge">Python</span>
            <span class="skill-badge">Apache Kafka</span>
            <span class="skill-badge">Apache Spark</span>
            <span class="skill-badge">Apache Airflow</span>
            <span class="skill-badge">PostgreSQL</span>
            <span class="skill-badge">dbt</span>
            <span class="skill-badge">Delta Lake</span>
            <span class="skill-badge">Docker</span>
            <span class="skill-badge">CI/CD</span>
            <span class="skill-badge">NLP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Metrics ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-value">5</div><div class="metric-label">Projects</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-value">150+</div><div class="metric-label">Files</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-value">36+</div><div class="metric-label">Unit Tests</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-value">15+</div><div class="metric-label">dbt Models</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # ── Project Cards ──
    st.markdown('<div class="section-header">🗂️ Projects</div>', unsafe_allow_html=True)

    projects = [
        {
            "icon": "🛍️", "title": "Real-Time E-Commerce Streaming Pipeline",
            "color": "#FF6B6B",
            "desc": "Kafka → Spark Structured Streaming → Delta Lake → dbt star schema. Simulates high-volume clickstream and order events with anomaly (bot) detection, dead-letter queues, and Medallion architecture.",
            "tech": ["Kafka", "PySpark", "Delta Lake", "dbt", "Airflow"],
        },
        {
            "icon": "🌤️", "title": "Weather Anomaly Detection Pipeline",
            "color": "#4ECDC4",
            "desc": "Pulls real weather data from the Open-Meteo API, detects temperature and wind anomalies using Z-score statistics, and fires alerts with cooldown windows. Physics-based quality gates and dbt marts.",
            "tech": ["REST API", "Z-Score", "PostgreSQL", "Airflow", "dbt"],
        },
        {
            "icon": "💼", "title": "Job Market Analytics Platform",
            "color": "#FFD93D",
            "desc": "Scrapes job postings, extracts 100+ skills via regex NLP taxonomy, normalizes multi-currency salaries with live FX rates, and builds a star schema for market intelligence.",
            "tech": ["NLP", "Regex Taxonomy", "Multi-Currency FX", "dbt", "Airflow"],
        },
        {
            "icon": "🏭", "title": "IoT Sensor Data Platform",
            "color": "#6C63FF",
            "desc": "Simulates 50 industrial sensors with drift, diurnal patterns, and random failures. 3-level time-series downsampling (1min→5min→1hr→1day), device health monitoring, and retention policies.",
            "tech": ["Time-Series", "Downsampling", "Device Health", "Parquet", "dbt"],
        },
        {
            "icon": "📱", "title": "Social Media Sentiment Data Lake",
            "color": "#00D4FF",
            "desc": "Bronze→Silver→Gold data lake. Lexicon-based sentiment analysis with negation handling and emoji boosting. Topic classification across 5 domains. Rolling-average trend spike detection.",
            "tech": ["Data Lake", "Sentiment NLP", "Trend Detection", "Parquet", "dbt"],
        },
    ]

    for p in projects:
        tech_badges = "".join(f'<span class="skill-badge">{t}</span>' for t in p["tech"])
        st.markdown(f"""
        <div class="project-card" style="border-left-color: {p['color']};">
            <div class="project-title">{p['icon']} {p['title']}</div>
            <div class="project-desc">{p['desc']}</div>
            <div style="margin-top:0.8rem;">{tech_badges}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Skills Matrix ──
    st.markdown('<div class="section-header">🧠 Technical Skills</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🔧 Core Engineering")
        st.markdown("""
        - Python (pandas, NumPy, PySpark)
        - SQL / PostgreSQL
        - Apache Airflow (DAGs, XCom)
        - Apache Kafka (Producers/Consumers)
        - Docker & Docker Compose
        """)
    with col2:
        st.markdown("#### 📊 Data Modeling")
        st.markdown("""
        - dbt Core (staging → marts)
        - Star Schema Design
        - Data Lake (Bronze/Silver/Gold)
        - Delta Lake / Parquet
        - Time-Series Engineering
        """)
    with col3:
        st.markdown("#### 🚀 Production Patterns")
        st.markdown("""
        - CI/CD (GitHub Actions)
        - Data Quality Gates
        - Error Handling & DLQ
        - Monitoring & Alerting
        - NLP & Sentiment Analysis
        """)

    # ── Architecture Patterns ──
    st.markdown('<div class="section-header">🏗️ Architecture Patterns Used</div>', unsafe_allow_html=True)

    arch_col1, arch_col2 = st.columns(2)
    with arch_col1:
        st.markdown("""
        | Pattern | Project |
        |---------|---------|
        | Medallion (Bronze/Silver/Gold) | P1, P5 |
        | Star Schema (fact + dimension) | P1, P2, P3, P4, P5 |
        | Multi-Granularity Downsampling | P4 |
        | Dead Letter Queue (DLQ) | P1 |
        | Anomaly Detection (Z-score) | P2 |
        """)
    with arch_col2:
        st.markdown("""
        | Pattern | Project |
        |---------|---------|
        | NLP Taxonomy Extraction | P3 |
        | Lexicon Sentiment Analysis | P5 |
        | Device Health Monitoring | P4 |
        | Alert Cooldown Windows | P2 |
        | Data Retention Policies | P4 |
        """)

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center; color:#8888a0; font-size:0.85rem;">'
        '👈 Select a project from the sidebar to see a <b>live interactive demo</b>'
        '</div>',
        unsafe_allow_html=True,
    )
