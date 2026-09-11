# 60-second explanation

I wanted to understand the data-engineering problem behind robotics training datasets, so I built a small pipeline around raw multimodal sensor events.

The source contains timestamped sensor records with IMU, force, camera-frame and task metadata. I applied an explicit schema, checked required fields and numeric validity, detected duplicates, and added a simple sensor-range rule. Valid records are written to a curated dataset and invalid records are isolated with rejection reasons. The pipeline also produces a quality report.

The important part is that I did not try to solve the robotics-model problem. I focused on reliable data processing and quality controls, which maps directly to my existing Data Engineering experience.

## Why duplicate detection?

A repeated event can inflate training data and distort downstream statistics, so the pipeline uses session + timestamp + frame as an event key.

## Why reject bad records instead of deleting them?

Rejected records are retained separately with reasons so the issue is observable and can be investigated or reprocessed.

## How would you productionize it?

Move raw files to ADLS Gen2/object storage, use Spark/Databricks for distributed processing, store curated datasets in Delta Lake, add orchestration, monitoring and CI/CD, and maintain dataset versions/releases.

## What is intentionally simplified?

The demo does not implement real camera/IMU synchronization, robotics calibration, ML training, or production-scale anomaly detection. Those require domain-specific requirements and data that are not available in this proof of concept.
