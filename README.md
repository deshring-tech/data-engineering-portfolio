# 🚀 Data Engineering Portfolio — Deshring Daulaguphu

Welcome to my interactive Data Engineering portfolio! This project showcases a series of production-grade data pipelines, ranging from real-time e-commerce streaming to job market analytics and weather anomaly detection.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://data-engineering-portfolio.streamlit.app/)

## 👨‍💻 About Me
I am a **Data Engineer / Analytics Engineer** with a strong background in digital business operations and an MBA in Digital Marketing. I specialize in architecting end-to-end data pipelines using modern data stacks.

- **Stack:** Python, SQL, Apache Spark, Kafka, dbt, Airflow, Delta Lake, Snowflake, Docker.
- **LinkedIn:** [My LinkedIn](https://www.linkedin.com/in/deshring-daulaguphu-0599a016b/) <!-- Update if needed -->
- **Location:** Diphu, India

## 🛠️ Included Projects

### 🛍️ 1. Real-Time E-Commerce Streaming
- **Scenario:** Processing high-volume clickstream events.
- **Tech:** Kafka → Spark Structured Streaming → Delta Lake → dbt.
- **Key Features:** Quality gate with bot detection and dead-letter queues.

### 🌤️ 2. Weather Anomaly Detection
- **Scenario:** Identifying meteorological anomalies in multi-city data.
- **Tech:** PostgreSQL → Airflow → dbt.
- **Key Features:** Physics-based data quality gates and Z-score anomaly tracking.

### 💼 3. Job Market Analytics (NLP)
- **Scenario:** Scraping and extracting market intelligence from job postings.
- **Tech:** Regex NLP → FX Normalization → dbt.
- **Key Features:** 100+ skill patterns and automated currency conversion.

## 🚀 How to Run Locally
Ensure you have Python 3.9+ installed, then:

```bash
# Clone the repository
git clone https://github.com/deshring-tech/data-engineering-portfolio.git
cd data-engineering-portfolio

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---
*Built with ❤️ using Streamlit*
