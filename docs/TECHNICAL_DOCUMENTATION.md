# Technical Documentation

## Repository structure

```text
.
├── app.py
├── README.md
├── DEPLOY.md
├── requirements.txt
├── requirements_streamlit.txt
├── data/
│   ├── raw/
│   │   └── sensor_events.csv
│   └── output/
│       ├── curated_sensor_events.csv
│       ├── rejected_sensor_events.csv
│       └── quality_report.md
├── docs/
│   ├── CASE_STUDY.md
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   ├── INTERVIEW_NOTES.md
│   └── LINKEDIN_POST.md
├── src/
│   ├── pipeline.py
│   └── pyspark_pipeline.py
└── tests/
    └── test_pipeline.py
```

## Execution

### Python pipeline

```bash
python src/pipeline.py
```

The command reads the raw CSV and writes:

- curated accepted records
- rejected records
- quality report

### Streamlit application

```bash
python -m streamlit run app.py
```

### PySpark pipeline

```bash
spark-submit src/pyspark_pipeline.py
```

## Validation flow

1. Read raw data.
2. Apply explicit schema.
3. Validate required fields.
4. Validate numeric fields.
5. Apply force range rule.
6. Detect duplicate event keys.
7. Assign `ACCEPT` or `REJECT`.
8. Write curated and rejected outputs.
9. Produce quality metrics.

## Data contract

| Field | Type | Purpose |
|---|---|---|
| session_id | string | Groups events into a session |
| timestamp_ms | integer | Event timestamp |
| camera_frame_id | string | Camera frame reference |
| imu_ax/ay/az | double | IMU measurements |
| force_n | double | Force measurement |
| action | string | Recorded action |
| object_name | string | Object involved |
| recorded_at | string | Recording timestamp |

## Production considerations

The POC uses CSV for portability. A production implementation should use durable object storage, a schema/data contract, distributed processing, transactional curated storage, orchestration and observability.

The illustrative force threshold should be replaced with limits based on actual sensor specifications and domain requirements.
