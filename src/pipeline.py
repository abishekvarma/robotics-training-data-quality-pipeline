import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/sensor_events.csv"
OUT = ROOT / "data/output"
OUT.mkdir(parents=True, exist_ok=True)

REQUIRED = ["session_id", "timestamp_ms", "camera_frame_id", "imu_ax", "imu_ay",
            "imu_az", "force_n", "action", "object_name", "recorded_at"]

def validate(row):
    errors = []
    for field in REQUIRED:
        if row.get(field, "") in ("", None):
            errors.append(f"missing:{field}")

    if errors:
        return errors

    try:
        ts = int(row["timestamp_ms"])
        if ts < 0:
            errors.append("invalid:timestamp_ms")
        for f in ("imu_ax", "imu_ay", "imu_az"):
            float(row[f])
        force = float(row["force_n"])
        if force < 0 or force > 100:
            errors.append("out_of_range:force_n")
    except ValueError:
        errors.append("invalid:numeric_value")

    return errors

def main():
    accepted, rejected = [], []
    seen = set()

    with RAW.open(newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        for row in rows:
            key = (row["session_id"], row["timestamp_ms"], row["camera_frame_id"])
            errors = validate(row)

            if key in seen:
                errors.append("duplicate:event")
            else:
                seen.add(key)

            if errors:
                row["rejection_reason"] = "|".join(errors)
                rejected.append(row)
            else:
                accepted.append(row)

    fields = REQUIRED
    with (OUT / "curated_sensor_events.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(accepted)

    with (OUT / "rejected_sensor_events.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields + ["rejection_reason"])
        w.writeheader()
        w.writerows(rejected)

    reasons = Counter()
    for row in rejected:
        reasons.update(row["rejection_reason"].split("|"))

    total = len(accepted) + len(rejected)
    report = [
        "# Data Quality Report\n",
        f"- Total records: {total}",
        f"- Accepted records: {len(accepted)}",
        f"- Rejected records: {len(rejected)}",
        f"- Acceptance rate: {(len(accepted)/total*100):.1f}%",
        "",
        "## Rejection reasons"
    ]
    report += [f"- {k}: {v}" for k, v in reasons.items()]
    (OUT / "quality_report.md").write_text("\n".join(report), encoding="utf-8")

    print("\n".join(report))

if __name__ == "__main__":
    main()
