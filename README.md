# Robotics Training Data Quality Pipeline

> **Data Engineering proof-of-concept:** raw multimodal sensor events → validation → quality gate → curated/rejected datasets → quality report.

## Why I built this

This project explores a Data Engineering problem relevant to robotics AI systems: creating reliable, training-ready datasets from raw multimodal sensor events.

I focused on the part that maps directly to my existing Data Engineering experience: ingestion, transformation, validation, deduplication and data-quality handling.

## Demo

Run locally:

```bash
pip install -r requirements_streamlit.txt
python -m streamlit run app.py
```

## Result

The included synthetic dataset contains **25 records**:

- **21 accepted**
- **4 rejected**
- **84% acceptance rate**

Rejected records include traceable reasons such as duplicate events, missing values and an illustrative out-of-range sensor value.

## Pipeline

```text
Raw multimodal events
        ↓
Explicit schema
        ↓
Required + numeric validation
        ↓
Duplicate + sensor-range checks
        ↓
 ┌───────────────┬────────────────┐
 ↓               ↓
Curated        Rejected
data           + reasons
        ↓
Training-ready dataset
```

## Documentation

- [Case Study](docs/CASE_STUDY.md)
- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md)
- [Data Quality Rules](docs/DATA_QUALITY_RULES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Interview Notes](docs/INTERVIEW_NOTES.md)
- [Portfolio Description](docs/PORTFOLIO_DESCRIPTION.md)
- [LinkedIn Post](docs/LINKEDIN_POST.md)

## Technology

**Implemented:** Python, PySpark, ETL, validation, data-quality rules, partitioned output.

**Production mapping:** ADLS Gen2, Azure Databricks, PySpark, Delta Lake, Azure Data Factory, automated monitoring.

Production mapping is an architectural proposal; this repository does not claim a production cloud deployment.

## Scope

This is a portfolio POC. It does not implement real robot hardware, camera/IMU synchronization, sensor calibration, robotics perception or ML training.

The goal is to demonstrate **reliable Data Engineering around multimodal data**.
