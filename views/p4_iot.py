"""
🏭 Project 4: IoT Sensor Data Platform — Live Demo
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


SENSOR_TYPES = {
    "temperature": {"baseline": 22.0, "noise": 1.5, "unit": "°C", "min": -10, "max": 100, "color": "#FF6B6B"},
    "humidity": {"baseline": 55.0, "noise": 3.0, "unit": "%", "min": 0, "max": 100, "color": "#4ECDC4"},
    "pressure": {"baseline": 1.0, "noise": 0.05, "unit": "bar", "min": 0.5, "max": 2.0, "color": "#6C63FF"},
    "vibration": {"baseline": 2.0, "noise": 0.8, "unit": "g", "min": 0, "max": 20, "color": "#FFD93D"},
    "power": {"baseline": 5.0, "noise": 1.0, "unit": "kW", "min": 0, "max": 50, "color": "#00D4FF"},
}


def simulate_fleet(n_devices: int = 30, hours: int = 24, failure_rate: float = 0.02, seed: int = 42):
    """Simulate IoT sensor fleet with drift + diurnal + failures."""
    rng = np.random.RandomState(seed)
    records = []
    timestamps = pd.date_range(end=datetime.now(), periods=hours * 60, freq="1min")

    for dev_idx in range(n_devices):
        stype_name = list(SENSOR_TYPES.keys())[dev_idx % len(SENSOR_TYPES)]
        stype = SENSOR_TYPES[stype_name]
        device_id = f"DEV-{dev_idx:04d}-{stype_name[:4].upper()}"
        drift = rng.uniform(-0.02, 0.08)
        battery = max(5, 100 - rng.uniform(0, 40) - dev_idx * 0.5)

        for i, ts in enumerate(timestamps):
            failed = rng.random() < failure_rate
            diurnal = np.sin(2 * np.pi * ts.hour / 24) * stype["noise"] * 0.5
            drift_val = drift * (i / len(timestamps))
            value = stype["baseline"] + diurnal + drift_val + rng.normal(0, stype["noise"])
            value = np.clip(value, stype["min"], stype["max"])

            records.append({
                "device_id": device_id, "sensor_type": stype_name,
                "timestamp": ts, "value": round(value, 3) if not failed else None,
                "unit": stype["unit"], "battery_pct": round(max(0, battery - i * 0.002), 1),
                "quality_flag": "good" if not failed else "device_error",
            })

    return pd.DataFrame(records)


def downsample(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    """Multi-granularity downsampling."""
    valid = df[df["value"].notna()].copy()
    valid["bucket"] = valid["timestamp"].dt.floor(freq)
    result = valid.groupby(["device_id", "sensor_type", "bucket"]).agg(
        avg_value=("value", "mean"), min_value=("value", "min"),
        max_value=("value", "max"), std_value=("value", "std"), count=("value", "count"),
    ).reset_index()
    result = result.round(3)
    return result


def render():
    st.markdown("""
    <div class="hero-container" style="background: linear-gradient(135deg, #1a1f2e 0%, #1b2a69 50%, #1a1f2e 100%);">
        <div class="hero-title" style="font-size:2rem;">🏭 IoT Sensor Data Platform</div>
        <div class="hero-subtitle">Fleet Simulation → Multi-Granularity Downsampling → Device Health</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📐 Architecture", expanded=False):
        st.markdown("""
        ```
        50-Device Fleet ──→ Raw Readings (1-min) ──→ Downsampler
                              │                         │
                        Device Registry        ┌────────┼────────┐
                              │              5-min    1-hour    1-day
                        Health Monitor          │        │        │
                              │            (30d ret) (365d ret) (forever)
                 ┌────────────┼────────────┐
              Heartbeat   Threshold    Error Rate
                              │
                        dbt → fct_sensor_hourly + dim_devices
        ```
        **Tech:** NumPy, pandas, PostgreSQL, dbt, Airflow, Docker
        """)

    st.markdown("### ⚙️ Configure Simulation")
    c1, c2, c3 = st.columns(3)
    with c1:
        n_devices = st.slider("Fleet size:", 5, 50, 20)
    with c2:
        hours = st.slider("Hours to simulate:", 1, 48, 12)
    with c3:
        failure_rate = st.slider("Failure rate %:", 0, 20, 3) / 100

    if st.button("🏭 Run Simulation", use_container_width=True, type="primary"):
        with st.spinner("Simulating sensor fleet..."):
            import random as rand_mod
            df = simulate_fleet(n_devices, hours, failure_rate, seed=rand_mod.randint(1, 9999))

        raw_count = len(df)
        error_count = (df["quality_flag"] == "device_error").sum()
        valid = df[df["value"].notna()]

        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Raw Readings", f"{raw_count:,}")
        m2.metric("Device Errors", f"{error_count:,}", delta=f"{error_count/raw_count*100:.1f}%", delta_color="inverse")
        m3.metric("Active Devices", df["device_id"].nunique())
        m4.metric("Avg Battery", f"{df['battery_pct'].mean():.1f}%")

        # ── Multi-Granularity Downsampling ──
        st.markdown("### 📉 Multi-Granularity Downsampling")
        ds_5m = downsample(valid, "5min")
        ds_1h = downsample(valid, "1h")
        ds_1d = downsample(valid, "1D")

        ds1, ds2, ds3, ds4 = st.columns(4)
        ds1.metric("1-min (raw)", f"{len(valid):,}")
        ds2.metric("5-min", f"{len(ds_5m):,}", delta=f"{(1-len(ds_5m)/len(valid))*100:.0f}% compression")
        ds3.metric("1-hour", f"{len(ds_1h):,}", delta=f"{(1-len(ds_1h)/len(valid))*100:.0f}% compression")
        ds4.metric("1-day", f"{len(ds_1d):,}", delta=f"{(1-len(ds_1d)/len(valid))*100:.0f}% compression")

        # ── Sensor Type Charts ──
        st.markdown("### 📊 Sensor Readings")
        selected_type = st.selectbox("Sensor type:", list(SENSOR_TYPES.keys()))
        type_data = valid[valid["sensor_type"] == selected_type]
        info = SENSOR_TYPES[selected_type]

        # Show first 3 devices of this type
        devices = type_data["device_id"].unique()[:3]
        fig = go.Figure()
        for dev in devices:
            dev_data = type_data[type_data["device_id"] == dev]
            fig.add_trace(go.Scatter(x=dev_data["timestamp"], y=dev_data["value"],
                                   mode="lines", name=dev, opacity=0.8))
        fig.update_layout(title=f"{selected_type.title()} — Raw Readings ({info['unit']})",
                         template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                         plot_bgcolor="rgba(0,0,0,0)", height=350)
        st.plotly_chart(fig, use_container_width=True)

        # ── Device Health ──
        st.markdown("### 🩺 Device Health Monitor")
        health = valid.groupby("device_id").agg(
            sensor_type=("sensor_type", "first"),
            avg_value=("value", "mean"), max_value=("value", "max"),
            reading_count=("value", "count"),
            battery=("battery_pct", "last"),
        ).reset_index()

        # Compute error rate per device
        err_df = df.groupby("device_id").agg(
            total=("quality_flag", "count"),
            errors=("quality_flag", lambda x: (x == "device_error").sum()),
        ).reset_index()
        err_df["error_rate"] = (err_df["errors"] / err_df["total"] * 100).round(1)
        health = health.merge(err_df[["device_id", "error_rate"]], on="device_id")

        health["status"] = "healthy"
        health.loc[health["battery"] < 15, "status"] = "low_battery"
        health.loc[health["error_rate"] > 10, "status"] = "degraded"

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            status_counts = health["status"].value_counts().reset_index()
            status_counts.columns = ["status", "count"]
            fig_h = px.pie(status_counts, names="status", values="count",
                          title="🩺 Fleet Health Status",
                          color_discrete_map={"healthy": "#4ECDC4", "low_battery": "#FFD93D", "degraded": "#FF6B6B"})
            fig_h.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig_h, use_container_width=True)

        with col_h2:
            fig_b = px.scatter(health, x="error_rate", y="battery", color="status",
                             size="reading_count", hover_data=["device_id", "sensor_type"],
                             title="🔋 Battery vs Error Rate",
                             color_discrete_map={"healthy": "#4ECDC4", "low_battery": "#FFD93D", "degraded": "#FF6B6B"})
            fig_b.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                              plot_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig_b, use_container_width=True)

        with st.expander("📄 Fleet Health Table", expanded=False):
            st.dataframe(health.sort_values("status").round(2), use_container_width=True, height=400)
