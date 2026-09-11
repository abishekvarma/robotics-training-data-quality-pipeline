import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import validate

def test_valid_row():
    row = {
        "session_id":"S1","timestamp_ms":"1","camera_frame_id":"F1",
        "imu_ax":"0.1","imu_ay":"0.2","imu_az":"9.7","force_n":"2.0",
        "action":"grasp","object_name":"cup","recorded_at":"2026-01-01T00:00:00"
    }
    assert validate(row) == []

def test_missing_force():
    row = {
        "session_id":"S1","timestamp_ms":"1","camera_frame_id":"F1",
        "imu_ax":"0.1","imu_ay":"0.2","imu_az":"9.7","force_n":"",
        "action":"grasp","object_name":"cup","recorded_at":"2026-01-01T00:00:00"
    }
    assert "missing:force_n" in validate(row)

def test_force_range():
    row = {
        "session_id":"S1","timestamp_ms":"1","camera_frame_id":"F1",
        "imu_ax":"0.1","imu_ay":"0.2","imu_az":"9.7","force_n":"150",
        "action":"grasp","object_name":"cup","recorded_at":"2026-01-01T00:00:00"
    }
    assert "out_of_range:force_n" in validate(row)
