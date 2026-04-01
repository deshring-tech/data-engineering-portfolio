"""
👨‍💻 Resume & About Me — Data Engineering Focus
"""
import streamlit as st
import os

def render():
    st.markdown("""
    <style>
    .resume-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FAFAFA;
        margin-bottom: 0;
    }
    .resume-subtitle {
        font-size: 1.2rem;
        color: #6C63FF;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .contact-info {
        color: #a0a0b8;
        font-size: 0.95rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #FAFAFA;
        border-bottom: 2px solid rgba(108, 99, 255, 0.3);
        padding-bottom: 0.3rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .job-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #00D4FF;
    }
    .job-company {
        font-size: 1rem;
        color: #FAFAFA;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .job-date {
        font-size: 0.9rem;
        color: #8888a0;
    }
    .resume-text {
        color: #d0d0e0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .resume-list li {
        margin-bottom: 0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Header Section ──
    col1, col2 = st.columns([1, 2.8])
    
    with col1:
        img_path_jpg = "assets/profile.jpg"
        img_path_png = "assets/profile.png"
        
        if os.path.exists(img_path_jpg):
            st.image(img_path_jpg, width=220)
        elif os.path.exists(img_path_png):
            st.image(img_path_png, width=220)
        else:
            st.info("💡 Place 'profile.jpg' in the 'assets' folder to show your photo here.")
            
        st.markdown("""
        <div class="contact-info">
            📍 Diphu, India<br>
            📧 deshring.info@gmail.com<br>
            📱 +91 8822065302<br>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="resume-header">Deshring Daulaguphu</div>', unsafe_allow_html=True)
        st.markdown('<div class="resume-subtitle">Data Engineer / Analytics Engineer</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="resume-text" style="margin-bottom: 1rem;">
        Dynamic and analytically-driven professional with an MBA and a strong foundation in digital business operations. 
        Successfully transitioned into Data Engineering by architecting and deploying multiple production-grade, end-to-end data pipelines. 
        Passionate about leveraging modern data stacks (Kafka, Spark, Airflow, dbt) to solve complex business problems, 
        build robust data lakes, and drive growth for tech-forward enterprises. 
        Brings a unique blend of business acumen, digital marketing analytics, and rigorous data infrastructure skills.
        </div>
        """, unsafe_allow_html=True)

    # ── Technical Skills ──
    st.markdown('<div class="section-title">Technical Skills</div>', unsafe_allow_html=True)
    
    sk_col1, sk_col2, sk_col3 = st.columns(3)
    with sk_col1:
        st.markdown("""
        <div class="resume-text">
        <b>Data Engineering Core</b><br>
        • Python, SQL / Postgres<br>
        • Apache Spark (PySpark)<br>
        • Apache Kafka<br>
        • dbt Core & Data Modeling<br>
        • Airflow (Orchestration)<br>
        </div>
        """, unsafe_allow_html=True)
    with sk_col2:
        st.markdown("""
        <div class="resume-text">
        <b>Data Architecture</b><br>
        • Delta Lake / Data Lakes<br>
        • Star Schema Design<br>
        • Medallion Architecture<br>
        • Time-Series Analysis<br>
        • Streaming & Batch Processing<br>
        </div>
        """, unsafe_allow_html=True)
    with sk_col3:
        st.markdown("""
        <div class="resume-text">
        <b>Tools & Analytics</b><br>
        • Docker & Docker Compose<br>
        • CI/CD (GitHub Actions)<br>
        • Google Analytics & Ads<br>
        • ChatGPT / Prompt Eng.<br>
        • Marketing Analytics<br>
        </div>
        """, unsafe_allow_html=True)

    # ── Experience ──
    st.markdown('<div class="section-title">Experience</div>', unsafe_allow_html=True)

    # Experience 1: Portfolio
    exp_c1, exp_c2 = st.columns([3, 1])
    with exp_c1:
        st.markdown('<div class="job-title">Data Engineering Portfolio Creator</div>', unsafe_allow_html=True)
        st.markdown('<div class="job-company">Independent Sabbatical & Upskilling Project</div>', unsafe_allow_html=True)
    with exp_c2:
        st.markdown('<div class="job-date">2023 – Present</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="resume-text">
    <ul class="resume-list">
        <li>Architected and deployed 5 production-grade data pipelines demonstrating expertise in modern data stacks.</li>
        <li><b>E-Commerce Streaming:</b> Built a real-time Kafka & PySpark pipeline simulating high-volume traffic with bot detection and dead-letter queues, processed into a Delta Lake and dbt star schema.</li>
        <li><b>Job Market NLP:</b> Scraped and extracted 100+ skills using regex taxonomies, normalizing multi-currency salaries via API integrations and modeling data with dbt and Airflow.</li>
        <li><b>Weather Anomalies:</b> Created a PostgreSQL/Airflow pipeline using Z-score statistics to detect meteorological anomalies with physics-based quality gates.</li>
        <li><b>IoT Sensors & Social Sentiment:</b> Engineered complex data lakes processing time-series downsampling, device health tracking, and lexicon-based NLP sentiment analysis.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Experience 2: Digital Business
    exp_c3, exp_c4 = st.columns([3, 1])
    with exp_c3:
        st.markdown('<div class="job-title">Independent Digital Business & Data Analyst</div>', unsafe_allow_html=True)
        st.markdown('<div class="job-company">Progressive Warrior Monster, Virtua Cryptic, Dropshipping Operations</div>', unsafe_allow_html=True)
    with exp_c4:
        st.markdown('<div class="job-date">2018 – Present</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="resume-text">
    <ul class="resume-list">
        <li>Built and scaled digital operations including e-commerce storefronts (Shopify, WordPress) and multiple YouTube channels focused on Crypto, Fitness, and MMA, growing audiences to 1,000+ subscribers.</li>
        <li>Utilized Google Analytics, YouTube Analytics, and Shopify data to study consumer behavior, identify market trends, and optimize content algorithms, driving viewership and conversion rates.</li>
        <li>Managed paid media campaigns (Google Ads, Meta Ads) leveraging empirical data to maximize ROI and lower customer acquisition costs.</li>
        <li>Conducted basic fundamental analysis and managed investments in stock and cryptocurrency markets.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Education & Certifications ──
    st.markdown('<div class="section-title">Education & Certifications</div>', unsafe_allow_html=True)

    edu_c1, edu_c2 = st.columns(2)
    with edu_c1:
        st.markdown("""
        <div class="resume-text">
        <b style="color:#FAFAFA;">Master of Business Administration (MBA)</b><br>
        <i>Asia Pacific Institute of Management, Delhi</i> | 2018- 2020<br>
        • Specialization: Digital Marketing<br>
        • Key Focus: Customer Relationship Management, Analytics, Strategic Operations
        </div>
        """, unsafe_allow_html=True)

    with edu_c2:
        st.markdown("""
        <div class="resume-text">
        <b style="color:#FAFAFA;">Bachelor of Business Administration (BBA)</b><br>
        <i>Kaziranga University</i> | 2013- 2016<br>
        • Major: Marketing<br>
        • Key Focus: Consumer Behavior, Service Marketing, General Management
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="resume-text">
    <b>Certifications:</b><br>
    • Google Digital Marketing Certification<br>
    • Basics of Project Management Course
    </div>
    """, unsafe_allow_html=True)
