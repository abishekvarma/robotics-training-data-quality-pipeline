# Case Study — Robotics Training Data Quality Pipeline

## 1. Context

This proof-of-concept explores a Data Engineering problem relevant to robotics AI systems: **how to turn raw multimodal sensor events into a reliable curated dataset without allowing obvious data-quality issues to pass downstream**.

The project is intentionally scoped to the Data Engineering layer. It does not attempt to reproduce a company's proprietary systems or build a robotics model.

## 2. Problem statement

A raw robotics event stream may contain camera-frame references, IMU measurements, force readings, actions, object metadata and timestamps.

Before downstream consumers can use that data, the pipeline should answer:

- Is the record structurally complete?
- Are numeric fields valid?
- Are sensor values within an expected range?
- Is this event duplicated?
- If a record is rejected, can an engineer understand why?

## 3. Proposed solution

The POC creates a quality gate:

```text
Raw sensor events
       ↓
Explicit schema
       ↓
Required-field + numeric validation
       ↓
Duplicate detection + sensor range checks
       ↓
 ┌───────────────┬────────────────┐
 │               │                │
 ▼               ▼                ▼
Accepted      Rejected       Quality report
 │               │
 ▼               ▼
Curated       Reason attached
dataset       to each failure
```

## 4. Dataset

The sample dataset contains 25 synthetic sensor-event records across multiple sessions.

Each event contains:

- `session_id`
- `timestamp_ms`
- `camera_frame_id`
- `imu_ax`, `imu_ay`, `imu_az`
- `force_n`
- `action`
- `object_name`
- `recorded_at`

The data is deliberately seeded with quality issues so the pipeline can demonstrate validation behavior.

## 5. Quality rules

### Required fields
A record is rejected if required fields such as timestamp or force are missing.

### Numeric validation
Sensor fields must be parseable as numeric values.

### Force range
The POC uses a simple illustrative range check for force values. In a real system, limits would come from sensor specifications and domain requirements.

### Duplicate detection
An event is considered duplicated when the combination of session, timestamp and camera frame identifies the same event more than once.

## 6. Result

For the included sample:

| Metric | Result |
|---|---:|
| Raw records | 25 |
| Accepted | 21 |
| Rejected | 4 |
| Acceptance rate | 84% |

The four rejected records demonstrate four different failure types:

1. duplicate event
2. missing force
3. force outside the illustrative range
4. missing timestamp

Rejected records are retained separately with a rejection reason.

## 7. Why this matters

The value is not the 25-row dataset itself. The value is the **pattern**:

> raw data should pass through explicit quality controls before becoming a downstream dataset.

At larger scale, the same pattern can be applied to much larger multimodal datasets with distributed processing, automated monitoring and dataset versioning.

## 8. Technology

### Implemented in the POC
- Python
- PySpark
- CSV-based raw input
- validation rules
- curated/rejected outputs
- quality report

### Production architecture considered
- ADLS Gen2 / cloud object storage
- Azure Databricks
- PySpark
- Delta Lake
- Azure Data Factory
- automated data-quality monitoring

The production technologies are architecture recommendations, not claims that they were deployed in this POC.

## 9. Engineering decisions

### Why retain rejected data?
Deleting bad records would remove evidence. Keeping them with reasons makes failures observable and allows investigation/reprocessing.

### Why separate curated and rejected outputs?
Downstream consumers should receive a predictable curated dataset while data-quality failures remain available for analysis.

### Why use an explicit schema?
Implicit type inference can hide inconsistent data. Explicit schemas make expectations visible and validation reproducible.

## 10. Limitations

This is a portfolio POC, so it does not implement:

- real robot hardware
- real camera/IMU synchronization
- sensor calibration
- robotics perception
- ML training
- production cloud deployment
- production monitoring/alerting
- a real company's internal data

Those areas require domain-specific data and requirements.

## 11. Future improvements

If this were extended toward production, I would add:

1. incremental ingestion
2. Delta Lake tables and schema evolution
3. data-quality metrics over time
4. automated alerts
5. pipeline orchestration
6. data lineage
7. dataset/version release tracking
8. scalable anomaly detection
9. automated tests in CI/CD

## 12. Interview takeaway

The strongest way to describe the project is:

> "I studied a robotics data-engineering problem and built a small proof-of-concept around the part that matches my existing experience: reliable ingestion, validation, quality checks, rejection handling and curated data delivery."

