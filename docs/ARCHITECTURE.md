# Architecture

```text
Raw multimodal events
        |
        v
+--------------------+
| Ingestion / Schema |
+--------------------+
        |
        v
+-----------------------------+
| Data Quality Validation     |
| - required fields           |
| - numeric validity          |
| - sensor range checks       |
| - duplicate detection       |
+-----------------------------+
        |
        +------------------+
        |                  |
        v                  v
   Curated data       Rejected data
        |                  |
        v                  v
 Partitioned output   Quality report
        |
        v
 Training-ready dataset
```

## Production mapping

The local CSV is a demonstration source. A production implementation could replace it with ADLS Gen2/object storage and use Delta Lake for ACID tables, schema enforcement, history and incremental processing.

The key engineering concept remains the same: **do not allow poor-quality raw data to silently reach downstream training datasets.**
