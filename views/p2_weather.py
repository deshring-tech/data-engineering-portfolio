"""
🌤️ Project 2: Weather Anomaly Detection Pipeline — Live Demo
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime, timedelta


def fetch_weather(lat: float, lon: float, days: int = 14):
    """Fetch real weather data from the Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": "temperature_2m,windspeed_10m,relative_humidity_2m",
        "past_days": days, "forecast_days": 1,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    hourly = data["hourly"]
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(hourly["time"]),
        "temperature_c": hourly["temperature_2m"],
        "wind_speed_kmh": hourly["windspeed_10m"],
        "humidity_pct": hourly["relative_humidity_2m"],
    })
    return df


def detect_anomalies(df: pd.DataFrame, column: str, z_threshold: float = 2.0):
    """Z-score anomaly detection."""
    mean = df[column].mean()
    std = df[column].std()
    df[f"{column}_zscore"] = ((df[column] - mean) / std).round(3)
    df[f"{column}_anomaly"] = df[f"{column}_zscore"].abs() > z_threshold
    return df, mean, std


PRESET_CITIES = {
    "Mumbai, India": (19.076, 72.8777),
    "New York, USA": (40.7128, -74.0060),
    "London, UK": (51.5074, -0.1278),
    "Tokyo, Japan": (35.6762, 139.6503),
    "Sydney, Australia": (-33.8688, 151.2093),
    "Dubai, UAE": (25.2048, 55.2708),
    "São Paulo, Brazil": (-23.5505, -46.6333),
}


def render():
    st.markdown("""
    <div class="hero-container" style="background: linear-gradient(135deg, #1a1f2e 0%, #1b4332 50%, #1a1f2e 100%);">
        <div class="hero-title" style="font-size:2rem;">🌤️ Weather Anomaly Detection</div>
        <div class="hero-subtitle">Open-Meteo API → Z-Score Analysis → Alert System</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📐 Architecture", expanded=False):
        st.markdown("""
        ```
        Open-Meteo API ──→ Raw Weather Data ──→ Z-Score Engine
                                                    │
                                            ┌───────┴────────┐
                                        Normal Data     Anomalies
                                            │               │
                                        PostgreSQL     Alert System
                                            │          (with cooldown)
                                      dbt Star Schema
                                            │
                                   fct_weather_hourly + dim_stations
        ```
        **Tech:** REST API, Z-Score, PostgreSQL, dbt, Airflow, pytest
        """)

    st.markdown("### 🌍 Select a Location")

    col1, col2 = st.columns([1, 1])
    with col1:
        city = st.selectbox("Preset city:", list(PRESET_CITIES.keys()))
    with col2:
        z_threshold = st.slider("Z-Score threshold:", 1.0, 4.0, 2.0, 0.5)

    lat, lon = PRESET_CITIES[city]
    st.caption(f"📍 Coordinates: {lat:.4f}, {lon:.4f}")

    if st.button("🔍 Fetch & Analyze Weather", use_container_width=True, type="primary"):
        with st.spinner(f"Fetching 14 days of weather data for {city}..."):
            try:
                df = fetch_weather(lat, lon, days=14)
            except Exception as e:
                st.error(f"API error: {e}")
                return

        # Run anomaly detection
        df, temp_mean, temp_std = detect_anomalies(df, "temperature_c", z_threshold)
        df, wind_mean, wind_std = detect_anomalies(df, "wind_speed_kmh", z_threshold)

        temp_anomalies = df["temperature_c_anomaly"].sum()
        wind_anomalies = df["wind_speed_kmh_anomaly"].sum()

        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Data Points", f"{len(df):,}")
        m2.metric("🌡️ Temp Anomalies", f"{temp_anomalies}", delta=f"{temp_anomalies/len(df)*100:.1f}%", delta_color="inverse")
        m3.metric("💨 Wind Anomalies", f"{wind_anomalies}", delta=f"{wind_anomalies/len(df)*100:.1f}%", delta_color="inverse")
        m4.metric("Avg Temperature", f"{temp_mean:.1f}°C")

        # Temperature chart with anomalies highlighted
        fig = go.Figure()
        normal = df[~df["temperature_c_anomaly"]]
        anomaly = df[df["temperature_c_anomaly"]]

        fig.add_trace(go.Scatter(x=normal["timestamp"], y=normal["temperature_c"],
                                mode="lines", name="Normal", line=dict(color="#6C63FF", width=1.5)))
        fig.add_trace(go.Scatter(x=anomaly["timestamp"], y=anomaly["temperature_c"],
                                mode="markers", name="🚨 Anomaly",
                                marker=dict(color="#FF6B6B", size=10, symbol="diamond")))

        # Mean ± threshold bands
        fig.add_hline(y=temp_mean, line_dash="dash", line_color="#4ECDC4",
                     annotation_text=f"Mean: {temp_mean:.1f}°C")
        fig.add_hline(y=temp_mean + z_threshold * temp_std, line_dash="dot", line_color="#FFD93D",
                     annotation_text=f"+{z_threshold}σ")
        fig.add_hline(y=temp_mean - z_threshold * temp_std, line_dash="dot", line_color="#FFD93D",
                     annotation_text=f"-{z_threshold}σ")

        fig.update_layout(title=f"🌡️ Temperature (14 Days) — {city}",
                         template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                         plot_bgcolor="rgba(0,0,0,0)", height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Wind speed
        col_l, col_r = st.columns(2)
        with col_l:
            fig2 = px.line(df, x="timestamp", y="wind_speed_kmh", title="💨 Wind Speed",
                          color_discrete_sequence=["#4ECDC4"])
            wind_anom = df[df["wind_speed_kmh_anomaly"]]
            fig2.add_trace(go.Scatter(x=wind_anom["timestamp"], y=wind_anom["wind_speed_kmh"],
                                     mode="markers", name="Anomaly",
                                     marker=dict(color="#FF6B6B", size=8)))
            fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig2, use_container_width=True)

        with col_r:
            fig3 = px.histogram(df, x="temperature_c_zscore", nbins=50,
                              title="📊 Temperature Z-Score Distribution",
                              color_discrete_sequence=["#6C63FF"])
            fig3.add_vline(x=z_threshold, line_dash="dash", line_color="#FF6B6B",
                          annotation_text=f"Threshold: {z_threshold}")
            fig3.add_vline(x=-z_threshold, line_dash="dash", line_color="#FF6B6B")
            fig3.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig3, use_container_width=True)

        with st.expander("📄 Anomaly Log", expanded=False):
            all_anom = df[df["temperature_c_anomaly"] | df["wind_speed_kmh_anomaly"]]
            if not all_anom.empty:
                st.dataframe(all_anom[["timestamp", "temperature_c", "temperature_c_zscore",
                                      "wind_speed_kmh", "wind_speed_kmh_zscore"]].head(30),
                            use_container_width=True)
            else:
                st.info("No anomalies detected at this threshold!")
