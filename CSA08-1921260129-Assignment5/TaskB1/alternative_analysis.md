# Measured pandas versus streaming CSV alternative

| Rows | CSV streaming time | CSV peak bytes | pandas time | pandas DataFrame bytes |
|---:|---:|---:|---:|---:|
| 1,000 | 0.0077 s | 45,253 | 0.0107 s | 119,132 |
| 100,000 | 0.8898 s | 49,038 | 0.0892 s | 11,900,132 |
| 1,000,000 | 9.7882 s | 48,958 | 0.9942 s | 119,000,132 |

The streaming method keeps only per-station totals and counts, so measured extra memory remains nearly constant. pandas is faster at larger sizes but stores the entire DataFrame. These values come from the included Python environment and will vary by computer.