"""
🚀 Data Engineering Portfolio — Interactive Dashboard
═════════════════════════════════════════════════════
A live, interactive showcase of 5 production-grade data engineering projects.
Recruiters can trigger real pipeline logic, see live charts, and explore data.
"""
import streamlit as st

# ══════════════════════════════════════════════
# Page Config
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="DE Portfolio — Dante",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
# Global CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
    /* ── Premium Dark Theme ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d1b69 50%, #1a1f2e 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(108, 99, 255, 0.2);
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.15);
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6C63FF, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #a0a0b8;
        margin-bottom: 1rem;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e2235 0%, #252a40 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(108, 99, 255, 0.15);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(108, 99, 255, 0.2);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #6C63FF;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8888a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Project Cards */
    .project-card {
        background: linear-gradient(145deg, #1e2235 0%, #252a40 100%);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .project-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .project-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #FAFAFA;
        margin-bottom: 0.4rem;
    }
    .project-desc {
        font-size: 0.9rem;
        color: #a0a0b8;
        line-height: 1.5;
    }

    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
        border: 1px solid rgba(108, 99, 255, 0.3);
        color: #c0c0e0;
        background: rgba(108, 99, 255, 0.1);
    }

    /* Section Headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #FAFAFA;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(108, 99, 255, 0.3);
    }

    /* Sidebar Styling */
    .css-1d391kg { padding-top: 2rem; }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# Session State Defaults
# ══════════════════════════════════════════════
if "currency" not in st.session_state:
    st.session_state["currency"] = "USD"

# ══════════════════════════════════════════════
# Sidebar
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🚀 Navigation")
    page = st.radio(
        "Choose a demo:",
        [
            "🏠 Home",
            "👨‍💻 Resume & About Me",
            "🛍️ E-commerce Streaming",
            "🌤️ Weather Anomalies",
            "💼 Job Market NLP",
            "🏭 IoT Sensors",
            "📱 Social Sentiment",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("#### 💱 Currency")
    selected_currency = st.radio(
        "Display prices in:",
        ["USD", "INR"],
        horizontal=True,
        index=0 if st.session_state["currency"] == "USD" else 1,
        key="currency_toggle",
    )
    st.session_state["currency"] = selected_currency
    if selected_currency == "INR":
        st.caption("Rate: 1 USD = ₹84")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; color:#8888a0; font-size:0.8rem;">
            Built with ❤️ using Streamlit<br>
            <a href="https://github.com/" style="color:#6C63FF;">GitHub</a> ·
            <a href="https://linkedin.com/" style="color:#6C63FF;">LinkedIn</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════
# Page Router
# ══════════════════════════════════════════════
if page == "🏠 Home":
    from views import home
    home.render()
elif page == "👨‍💻 Resume & About Me":
    from views import resume
    resume.render()
elif page == "🛍️ E-commerce Streaming":
    from views import p1_ecommerce
    p1_ecommerce.render()
elif page == "🌤️ Weather Anomalies":
    from views import p2_weather
    p2_weather.render()
elif page == "💼 Job Market NLP":
    from views import p3_jobs
    p3_jobs.render()
elif page == "🏭 IoT Sensors":
    from views import p4_iot
    p4_iot.render()
elif page == "📱 Social Sentiment":
    from views import p5_sentiment
    p5_sentiment.render()
