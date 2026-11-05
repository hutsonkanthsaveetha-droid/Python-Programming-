| Failure | Likely exception | Handling |
|---|---|---|
| Input directory missing | `FileNotFoundError` | Report directory issue; stop this batch cleanly |
| One daily file missing | `FileNotFoundError` | Log file; continue other files |
| Access denied | `PermissionError` | Log permission issue |
| Invalid UTF-8 bytes | `UnicodeDecodeError` | Log decoding problem; do not silently skip |
| Missing or extra fields | `InvalidRecord` (custom) | Catch per line and continue |
| Non-numeric field where numeric parsing is used | `ValueError` | Catch and record line |
| Indexing a missing field | `IndexError` | Prevent by validating field count before access |
| Empty file | No exception | Produce zero counts and an empty damaged-line list |
| Disk full / device error | `OSError` | Record at batch level if error log remains writable |
