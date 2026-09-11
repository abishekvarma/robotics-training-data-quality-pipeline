import csv
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Robotics Data Quality | Data Engineering POC",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
rejected_file = ROOT / "data/output/rejected_sensor_events.csv"
curated_file = ROOT / "data/output/curated_sensor_events.csv"

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 1.4rem 1.6rem; border-radius: 14px; border: 1px solid #e6e6e6; background: #fafafa;}
.kicker {font-size: .82rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;}
.muted {color: #666;}
.card {padding: 1rem 1.1rem; border: 1px solid #e8e8e8; border-radius: 12px; height: 100%;}
.step {padding: .85rem 1rem; border-left: 4px solid #555; background: #fafafa; margin-bottom: .55rem; border-radius: 6px;}
.small {font-size: .9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<div class="kicker">DATA ENGINEERING PROOF OF CONCEPT</div>
<h1 style="margin:.25rem 0 .35rem 0;">Robotics Training Data Quality Pipeline</h1>
<p class="muted" style="font-size:1.05rem;">
A practical pipeline for validating raw multimodal sensor events before they reach a curated,
training-ready dataset.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")
tabs = st.tabs(["Overview", "Quality Results", "Architecture", "Production Design", "Interview Story"])

with tabs[0]:
    st.subheader("The problem")
    st.write(
        "Raw robotics data can contain missing values, duplicate events and invalid sensor measurements. "
        "The goal of this POC is to create a reliable data-quality gate between raw events and downstream datasets."
    )

    st.subheader("What this POC does")
    cols = st.columns(4)
    cards = [
        ("01", "Ingest", "Read raw sensor events with an explicit schema."),
        ("02", "Validate", "Check required fields, numeric values and sensor ranges."),
        ("03", "Separate", "Keep accepted data apart from rejected records."),
        ("04", "Explain", "Attach rejection reasons and generate a quality report."),
    ]
    for c, (n, title, desc) in zip(cols, cards):
        with c:
            st.markdown(f'<div class="card"><b>{n} · {title}</b><p class="small">{desc}</p></div>', unsafe_allow_html=True)

    st.write("")
    st.subheader("Technology")
    st.markdown("**Python · PySpark · ETL · Data Quality · SQL concepts · Partitioned data · Azure production mapping**")

with tabs[1]:
    st.subheader("Pipeline result")
    cols = st.columns(4)
    cols[0].metric("Raw records", "25")
    cols[1].metric("Accepted", "21")
    cols[2].metric("Rejected", "4")
    cols[3].metric("Acceptance rate", "84%")

    st.write("")
    st.subheader("Why were records rejected?")
    reasons = {
        "Duplicate event": 1,
        "Missing force": 1,
        "Force out of range": 1,
        "Missing timestamp": 1,
    }
    rcols = st.columns(4)
    for c, (label, value) in zip(rcols, reasons.items()):
        with c:
            st.markdown(f'<div class="card"><b>{label}</b><h2>{value}</h2><span class="muted">record</span></div>', unsafe_allow_html=True)

    st.write("")
    st.subheader("Rejected records — with traceable reasons")
    if rejected_file.exists():
        with rejected_file.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        st.dataframe(rows, use_container_width=True, hide_index=True)

    st.caption("The sample dataset intentionally contains quality issues so the validation logic can be demonstrated.")

with tabs[2]:
    st.subheader("Logical architecture")
    st.code("""RAW MULTIMODAL SENSOR EVENTS
          │
          ▼
┌───────────────────────────┐
│ Ingestion + Explicit      │
│ Schema                    │
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│ Data Quality Gate         │
│ • required fields         │
│ • numeric validity        │
│ • sensor range checks     │
│ • duplicate detection     │
└─────────────┬─────────────┘
              │
       ┌──────┴──────┐
       ▼             ▼
   ACCEPT          REJECT
       │             │
       ▼             ▼
  CURATED DATA   REJECTED DATA
       │          + reason
       ▼
TRAINING-READY DATASET
""", language="text")

    st.subheader("Key engineering decision")
    st.info(
        "Rejected records are not silently deleted. They are isolated with a reason so the failure is "
        "observable and can be investigated or reprocessed."
    )

with tabs[3]:
    st.subheader("How I would productionize it")
    st.markdown("""
**Raw layer** → ADLS Gen2 / cloud object storage  
**Processing** → Azure Databricks + PySpark  
**Curated layer** → Delta Lake  
**Orchestration** → Azure Data Factory  
**Quality & monitoring** → automated checks, metrics and alerts  
**Dataset delivery** → versioned curated datasets
""")
    st.subheader("What this POC does — and does not — claim")
    st.success("Implemented: ingestion, schema validation, quality rules, duplicate detection, rejection tracking, curated output and PySpark processing.")
    st.warning("Not implemented in this local POC: real robot hardware, camera/IMU synchronization, robotics calibration, ML training, or a production cloud deployment.")

with tabs[4]:
    st.subheader("60-second explanation")
    st.write(
        "I wanted to understand the data-engineering problem behind robotics training datasets, so I built a "
        "small pipeline around raw multimodal sensor events. I applied an explicit schema, checked required "
        "fields and numeric validity, detected duplicates, added a sensor-range rule, and separated accepted "
        "records from rejected records with traceable reasons. The result is a curated dataset plus a quality "
        "report. I intentionally focused on the data-engineering layer because it maps directly to my existing "
        "pipeline and data-quality experience."
    )
    st.subheader("If asked: how would you scale it?")
    st.write(
        "I would move the raw layer to ADLS Gen2, process at scale with Databricks/PySpark, use Delta Lake "
        "for curated data and history, orchestrate with ADF, and add automated quality metrics, monitoring and alerts."
    )

st.divider()
st.caption("Portfolio POC • Built to demonstrate transferable Data Engineering skills, not to reproduce any company's proprietary system.")
