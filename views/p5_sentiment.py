"""
📱 Project 5: Social Media Sentiment Data Lake — Live Demo
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
import random
import uuid
from datetime import datetime, timedelta, timezone


# ── Sentiment Lexicon ──
POSITIVE_WORDS = {
    "amazing", "awesome", "best", "brilliant", "excellent", "fantastic", "great",
    "impressive", "incredible", "love", "outstanding", "perfect", "superb",
    "wonderful", "exciting", "remarkable", "innovative", "beautiful", "delightful",
    "breakthrough", "revolutionary", "game changer", "bright", "proud", "thrilled",
    "recommend", "success", "happy", "grateful", "optimistic",
}
NEGATIVE_WORDS = {
    "awful", "bad", "boring", "broken", "crash", "disaster", "disappointing",
    "failure", "hate", "horrible", "mess", "nightmare", "pathetic", "poor",
    "terrible", "toxic", "unacceptable", "waste", "worse", "worst", "angry",
    "frustrated", "disgusting", "scam", "useless", "worthless", "catastrophe",
}
POSITIVE_EMOJIS = {"🚀", "🎉", "💯", "❤️", "👏", "🔥", "✨", "💪", "👍", "🎊"}
NEGATIVE_EMOJIS = {"😤", "😡", "💀", "👎", "🤮", "😠", "💩", "🙄", "😞", "😢"}
NEGATION_WORDS = {"not", "no", "never", "don't", "doesn't", "didn't", "won't",
                   "can't", "couldn't", "shouldn't"}

TOPIC_TAXONOMY = {
    "technology": ["AI", "machine learning", "cloud", "kubernetes", "python", "javascript",
                    "startup", "SaaS", "API", "database", "open source", "GPT", "LLM"],
    "business": ["earnings", "revenue", "IPO", "stock", "market", "CEO", "layoff",
                  "acquisition", "funding", "valuation"],
    "politics": ["election", "policy", "government", "vote", "congress", "regulation", "tax"],
    "sports": ["game", "score", "championship", "FIFA", "NBA", "NFL", "Olympics", "cricket"],
    "entertainment": ["movie", "film", "Netflix", "series", "album", "concert", "Oscar", "Grammy"],
}

PLATFORMS = ["twitter", "reddit", "news", "youtube", "mastodon"]

POST_TEMPLATES = {
    "positive": [
        "Really impressed by the latest {kw}! This is a game changer 🚀",
        "Great news about {kw}. The future looks bright! 🎉",
        "{kw} is absolutely amazing. Can't believe how far we've come! 💯",
    ],
    "negative": [
        "Really disappointed with {kw}. Expected much better. 😤",
        "{kw} is a complete disaster. What were they thinking?",
        "Terrible experience with {kw}. Would not recommend. 😡",
    ],
    "neutral": [
        "Interesting developments around {kw}. Let's see how it plays out.",
        "New report on {kw} — some mixed results, worth reading.",
        "Looking at the data on {kw}. Not sure what to think yet.",
    ],
}


def score_sentiment(text: str) -> dict:
    """Score text sentiment using lexicon + emoji + negation."""
    text_lower = text.lower()
    words = set(re.findall(r'\b\w+\b', text_lower))

    pos = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    pos += sum(1 for e in POSITIVE_EMOJIS if e in text)
    neg += sum(1 for e in NEGATIVE_EMOJIS if e in text)

    has_negation = bool(NEGATION_WORDS & words)
    if has_negation:
        pos, neg = neg, pos

    total = pos + neg
    score = (pos - neg) / total if total else 0.0
    label = "positive" if score > 0.3 else ("negative" if score < -0.3 else "neutral")

    return {"score": round(score, 3), "label": label, "positive_signals": pos,
            "negative_signals": neg, "has_negation": has_negation}


def classify_topic(text: str) -> dict:
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPIC_TAXONOMY.items():
        scores[topic] = sum(1 for kw in keywords if kw.lower() in text_lower)

    if max(scores.values(), default=0) == 0:
        return {"topic": "unknown", "confidence": 0.0}
    best = max(scores, key=scores.get)
    return {"topic": best, "confidence": round(scores[best] / max(sum(scores.values()), 1), 3)}


def generate_batch(n: int = 500, seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)
    posts = []
    base = datetime.now(tz=timezone.utc) - timedelta(days=14)
    for _ in range(n):
        sentiment = rng.choices(["positive", "negative", "neutral"], weights=[35, 25, 40])[0]
        topic = rng.choice(list(TOPIC_TAXONOMY.keys()))
        kw = rng.choice(TOPIC_TAXONOMY[topic])
        template = rng.choice(POST_TEMPLATES[sentiment])
        text = template.format(kw=kw)
        platform = rng.choice(PLATFORMS)
        ts = base + timedelta(hours=rng.randint(0, 336))
        engagement = max(0, int(rng.expovariate(1 / (50 * (2.0 if sentiment == "negative" else 1.0)))))

        result = score_sentiment(text)
        topic_info = classify_topic(text)

        posts.append({
            "post_id": str(uuid.uuid4())[:8], "platform": platform, "text": text,
            "timestamp": ts, "engagement": engagement, "ground_truth": sentiment,
            "predicted": result["label"], "score": result["score"], "topic": topic_info["topic"],
        })
    return pd.DataFrame(posts)


def render():
    st.markdown("""
    <div class="hero-container" style="background: linear-gradient(135deg, #1a1f2e 0%, #0a3d62 50%, #1a1f2e 100%);">
        <div class="hero-title" style="font-size:2rem;">📱 Social Media Sentiment Lake</div>
        <div class="hero-subtitle">Bronze → Silver → Gold · Lexicon NLP · Trend Detection</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📐 Architecture", expanded=False):
        st.markdown("""
        ```
        Multi-Platform Posts ──→ Bronze (raw Parquet)
                                    │
                            Sentiment Pipeline
                          (lexicon + emoji + negation)
                                    │
                            Silver (enriched Parquet)
                                    │
                            Trend Detector
                         (7-day rolling avg spikes)
                                    │
                            Gold (aggregated) → PostgreSQL → dbt
        ```
        **Tech:** NLP, Parquet Partitioning, Rolling-Average Trends, dbt, Airflow
        """)

    # ── Tab 1: Live Analyzer ──
    tab1, tab2 = st.tabs(["🔍 Live Sentiment Analyzer", "📊 Batch Analytics"])

    with tab1:
        st.markdown("### Type anything and see the sentiment engine at work")

        user_text = st.text_area(
            "Enter text:",
            value="Really impressed by the latest AI breakthroughs! This is amazing 🚀",
            height=100, key="live_sentiment",
        )

        if st.button("🧠 Analyze Sentiment", use_container_width=True, type="primary"):
            result = score_sentiment(user_text)
            topic = classify_topic(user_text)

            # Visual score meter
            score = result["score"]
            color = "#4ECDC4" if score > 0.3 else ("#FF6B6B" if score < -0.3 else "#FFD93D")

            col1, col2, col3 = st.columns(3)
            col1.metric("Sentiment", result["label"].upper(), delta=f"Score: {score}")
            col2.metric("Topic", topic["topic"].title(), delta=f"Conf: {topic['confidence']}")
            col3.metric("Negation Detected", "Yes ⚡" if result["has_negation"] else "No")

            # Score gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Sentiment Score"},
                gauge={
                    "axis": {"range": [-1, 1]},
                    "bar": {"color": color},
                    "steps": [
                        {"range": [-1, -0.3], "color": "rgba(255,107,107,0.2)"},
                        {"range": [-0.3, 0.3], "color": "rgba(255,217,61,0.2)"},
                        {"range": [0.3, 1], "color": "rgba(78,205,196,0.2)"},
                    ],
                    "threshold": {"line": {"color": "white", "width": 2}, "thickness": 0.8, "value": score},
                },
            ))
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=250)
            st.plotly_chart(fig, use_container_width=True)

            # Signal breakdown
            st.markdown("#### 🔬 Analysis Breakdown")
            bc1, bc2 = st.columns(2)
            with bc1:
                st.markdown(f"""
                | Signal | Count |
                |--------|-------|
                | ✅ Positive words/emoji | **{result['positive_signals']}** |
                | ❌ Negative words/emoji | **{result['negative_signals']}** |
                | 🔄 Negation flip | **{'Yes' if result['has_negation'] else 'No'}** |
                """)
            with bc2:
                matched_pos = [w for w in POSITIVE_WORDS if w in user_text.lower()]
                matched_neg = [w for w in NEGATIVE_WORDS if w in user_text.lower()]
                matched_emojis_p = [e for e in POSITIVE_EMOJIS if e in user_text]
                matched_emojis_n = [e for e in NEGATIVE_EMOJIS if e in user_text]

                if matched_pos or matched_emojis_p:
                    st.success(f"Positive signals: {', '.join(matched_pos + matched_emojis_p)}")
                if matched_neg or matched_emojis_n:
                    st.error(f"Negative signals: {', '.join(matched_neg + matched_emojis_n)}")
                if not matched_pos and not matched_neg and not matched_emojis_p and not matched_emojis_n:
                    st.info("No strong sentiment signals detected → Neutral")

    with tab2:
        st.markdown("### 📊 Simulate 500 Posts & Analyze Trends")

        if st.button("📱 Generate & Analyze Batch", use_container_width=True, type="primary", key="batch"):
            with st.spinner("Generating 500 social media posts..."):
                df = generate_batch(500, seed=random.randint(1, 9999))

            # Accuracy
            accuracy = (df["ground_truth"] == df["predicted"]).mean()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Posts Generated", len(df))
            m2.metric("Platforms", df["platform"].nunique())
            m3.metric("Accuracy", f"{accuracy:.1%}")
            m4.metric("Topics", df["topic"].nunique())

            # Sentiment by platform
            col1, col2 = st.columns(2)
            with col1:
                plat_sent = df.groupby(["platform", "predicted"]).size().reset_index(name="count")
                fig_ps = px.bar(plat_sent, x="platform", y="count", color="predicted",
                              title="🌐 Sentiment by Platform", barmode="stack",
                              color_discrete_map={"positive": "#4ECDC4", "negative": "#FF6B6B", "neutral": "#FFD93D"})
                fig_ps.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                   plot_bgcolor="rgba(0,0,0,0)", height=350)
                st.plotly_chart(fig_ps, use_container_width=True)

            with col2:
                topic_sent = df.groupby("topic")["score"].mean().reset_index()
                topic_sent = topic_sent.sort_values("score")
                fig_ts = px.bar(topic_sent, x="score", y="topic", orientation="h",
                              title="📈 Average Sentiment by Topic",
                              color="score", color_continuous_scale="RdYlGn", color_continuous_midpoint=0)
                fig_ts.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                                   plot_bgcolor="rgba(0,0,0,0)", height=350)
                st.plotly_chart(fig_ts, use_container_width=True)

            # Trend detection
            st.markdown("### 🔥 Trend Detection")
            df["date"] = pd.to_datetime(df["timestamp"]).dt.date
            daily = df.groupby(["topic", "date"]).size().reset_index(name="count")
            fig_t = px.line(daily, x="date", y="count", color="topic",
                          title="📅 Daily Post Volume by Topic",
                          color_discrete_sequence=px.colors.qualitative.Set2)
            fig_t.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                              plot_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig_t, use_container_width=True)

            # Engagement vs sentiment scatter
            fig_e = px.scatter(df, x="score", y="engagement", color="predicted",
                             size="engagement", hover_data=["platform", "topic"],
                             title="💬 Engagement vs Sentiment Score",
                             color_discrete_map={"positive": "#4ECDC4", "negative": "#FF6B6B", "neutral": "#FFD93D"})
            fig_e.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                              plot_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig_e, use_container_width=True)

            with st.expander("📄 Sample Posts", expanded=False):
                st.dataframe(df[["platform", "text", "predicted", "score", "topic", "engagement"]].head(20),
                            use_container_width=True, height=400)
