"""
🛍️ Project 1: Real-Time E-Commerce Streaming Pipeline — Live Demo
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import random
import uuid
from datetime import datetime, timedelta


# ── Currency helper ──
INR_RATE = 84  # 1 USD = 84 INR

def fmt_currency(value: float) -> str:
    """Format a USD value according to the active session currency."""
    import streamlit as _st
    cur = _st.session_state.get("currency", "USD")
    if cur == "INR":
        return f"\u20b9{value * INR_RATE:,.0f}"
    return f"${value:,.2f}"


def get_price_col() -> str:
    """Return the active price column name for display."""
    import streamlit as _st
    return "price_inr" if _st.session_state.get("currency", "USD") == "INR" else "price_usd"


def generate_events(n_events: int = 200, seed: int = 42):
    """Simulate a burst of e-commerce clickstream + order events."""
    rng = np.random.RandomState(seed)
    categories = ["electronics", "clothing", "home", "sports", "beauty"]
    actions = ["view", "click", "add_to_cart", "purchase"]
    action_weights = [0.50, 0.25, 0.15, 0.10]

    events = []
    base_time = datetime.now() - timedelta(hours=1)
    for i in range(n_events):
        ts = base_time + timedelta(seconds=rng.randint(0, 3600))
        user_id = f"user_{rng.randint(1, 50):04d}"
        is_bot = rng.random() < 0.05
        action = rng.choice(actions, p=action_weights)
        cat = rng.choice(categories)
        price = round(rng.lognormal(3.5, 1.0), 2) if action == "purchase" else 0

        events.append({
            "event_id": str(uuid.uuid4())[:8],
            "timestamp": ts,
            "user_id": user_id if not is_bot else f"bot_{rng.randint(1,5):03d}",
            "action": action,
            "category": cat,
            "price_usd": price,
            "session_duration_s": rng.randint(2, 600) if not is_bot else rng.randint(0, 3),
            "is_bot": is_bot,
            "quality_flag": "good" if not is_bot else "suspicious",
        })

    return pd.DataFrame(events).sort_values("timestamp").reset_index(drop=True)


def render():
    st.markdown("""
    <div class="hero-container" style="background: linear-gradient(135deg, #1a1f2e 0%, #4a1942 50%, #1a1f2e 100%);">
        <div class="hero-title" style="font-size:2rem;">🛍️ Real-Time E-Commerce Streaming</div>
        <div class="hero-subtitle">Kafka → Spark Structured Streaming → Delta Lake → dbt</div>
    </div>
    """, unsafe_allow_html=True)

    # Architecture
    with st.expander("📐 Architecture", expanded=False):
        st.markdown("""
        ```
        Clickstream Events ──→ Kafka Topic ──→ Spark Structured Streaming
                                                    │
                                            ┌───────┴────────┐
                                            │  Quality Gate   │
                                            ├────────┬────────┤
                                         ✅ Good    ❌ Bot/Bad
                                            │           │
                                      Delta Bronze    DLQ Topic
                                            │
                                      Delta Silver (deduped, enriched)
                                            │
                                      Delta Gold (aggregated)
                                            │
                                      dbt Star Schema (facts + dims)
        ```
        **Tech:** Kafka, PySpark, Delta Lake, dbt, Airflow, Docker, GitHub Actions
        """)

    st.markdown("### ⚡ Live Simulation")
    st.markdown("Click the button to simulate a burst of e-commerce events and see the pipeline process them in real-time.")

    c1, c2 = st.columns([1, 1])
    with c1:
        n_events = st.slider("Number of events", 50, 1000, 300, step=50)
    with c2:
        bot_rate = st.slider("Bot traffic %", 0, 30, 5)

    if st.button("🚀 Simulate Traffic Burst", use_container_width=True, type="primary"):
        with st.spinner("Generating clickstream events..."):
            df = generate_events(n_events, seed=random.randint(1, 9999))
            # Adjust bot rate
            mask = np.random.random(len(df)) < (bot_rate / 100)
            df.loc[mask, "is_bot"] = True
            df.loc[mask, "quality_flag"] = "suspicious"
            df.loc[mask, "session_duration_s"] = np.random.randint(0, 3, size=mask.sum())

        # ── Metrics Row ──
        cur = st.session_state.get("currency", "USD")
        total = len(df)
        bots = df["is_bot"].sum()
        orders = (df["action"] == "purchase").sum()
        revenue = df["price_usd"].sum()

        # Add INR column for downstream use
        df["price_inr"] = (df["price_usd"] * INR_RATE).round(0)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Events", f"{total:,}")
        m2.metric("🤖 Bot Events", f"{bots}", delta=f"{bots/total*100:.1f}%", delta_color="inverse")
        m3.metric("🛒 Orders", f"{orders}")
        m4.metric("💰 Revenue", fmt_currency(revenue))

        # ── Charts ──
        col_left, col_right = st.columns(2)

        with col_left:
            # Event timeline
            df["minute"] = df["timestamp"].dt.floor("5min")
            timeline = df.groupby(["minute", "quality_flag"]).size().reset_index(name="count")
            fig = px.area(timeline, x="minute", y="count", color="quality_flag",
                         color_discrete_map={"good": "#6C63FF", "suspicious": "#FF6B6B"},
                         title="📊 Event Stream (5-min buckets)")
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            # Funnel
            funnel_data = df[~df["is_bot"]].groupby("action").size().reset_index(name="count")
            order = {"view": 0, "click": 1, "add_to_cart": 2, "purchase": 3}
            funnel_data["order"] = funnel_data["action"].map(order)
            funnel_data = funnel_data.sort_values("order")
            fig2 = go.Figure(go.Funnel(
                y=funnel_data["action"], x=funnel_data["count"],
                marker=dict(color=["#6C63FF", "#8B83FF", "#ABA3FF", "#00D4FF"]),
            ))
            fig2.update_layout(title="🔽 Conversion Funnel (Clean Traffic)",
                             template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # Category breakdown
        col3, col4 = st.columns(2)
        with col3:
            price_col = get_price_col()
            sym = "₹" if cur == "INR" else "$"
            cat_rev = df[df["action"] == "purchase"].groupby("category")[price_col].sum().reset_index()
            fig3 = px.bar(cat_rev, x="category", y=price_col, color="category",
                         title=f"💰 Revenue by Category ({cur})",
                         labels={price_col: f"Revenue ({sym})"},
                         color_discrete_sequence=px.colors.qualitative.Set2)
            fig3.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)", height=300, showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            # Bot vs Clean session duration
            fig4 = px.histogram(df, x="session_duration_s", color="quality_flag",
                              nbins=30, title="⏱️ Session Duration Distribution",
                              color_discrete_map={"good": "#6C63FF", "suspicious": "#FF6B6B"},
                              barmode="overlay", opacity=0.7)
            fig4.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig4, use_container_width=True)

        # Raw data preview
        with st.expander("📄 Raw Event Data (Bronze Layer)", expanded=False):
            # Show the active-currency price column; hide the other
            hide_col = "price_inr" if cur == "USD" else "price_usd"
            display_df = df.drop(columns=["minute", hide_col], errors="ignore").head(20)
            st.dataframe(display_df, use_container_width=True, height=400)
