# Data Quality Rules

| Rule | Condition | Action | Reason |
|---|---|---|---|
| Required fields | Required field is null/empty | Reject | `missing:<field>` |
| Numeric values | Numeric sensor value cannot be parsed | Reject | `invalid:numeric_value` |
| Force range | Force < 0 or > 100 in this demo | Reject | `out_of_range:force_n` |
| Duplicate event | Same session + timestamp + frame appears more than once | Reject | `duplicate:event` |

**Important:** the force threshold is intentionally illustrative. It is not presented as a real robotics sensor specification.
