# B4 - Final engineering decision

The prepared complaint fixture contains 51 short citizen messages with reference labels for demonstration. The word-list scorer agreed with 46 of 51 reference labels (90.2%). This is a small, prepared sample, not a validated city-wide accuracy estimate. Sarcasm, mixed opinions, double negation and local expressions require human review or a trained classifier with representative labelled data.

The extractive summariser selects sentences using important-word frequencies and retains the original wording. Its output is saved in `complaint_summary.txt`. For the alternative first-five baseline, the top-15 important-term coverage is 13/15 (86.7%), compared with 9/15 (60.0%) for the frequency-based summary. The simple baseline happens to cover more frequent terms on this sample; this is a dataset-specific result, not proof that first-five is generally better. With fixed k, first-k retrieval is O(1) with respect to corpus size and O(1) extra working space; frequency scoring is O(W) time for W words and O(V+S) space for vocabulary/sentence counts.

The composite primary key already creates an SQLite index beginning with `(station_id, day, hour)`. The explicit `(station_id, day)` index is therefore largely overlapping. The query plan before and after is recorded, and the measured timings are in `decision_results.txt`; small timing differences should be interpreted cautiously because the query is short and warmed caches reduce noise. The explicit index adds storage/write overhead and may not justify itself if the primary-key index serves the same filter.

## Production decision for 100 additional stations and 50,000 complaints/month
- Keep station metadata and timestamped readings in SQLite for the current scale, with a station/day index, parameterised SQL and monthly retention/backup. At much higher write concurrency, move to a managed relational/time-series database.
- Ingest files incrementally, validate schemas/encodings, convert units, deduplicate by station/time, median-impute only where defensible, and retain a rejected/imputed audit log.
- Use SQL aggregation for daily/monthly reports and pandas for exploratory analysis; schedule chart generation and monitor missing/rejected rates.
- Keep the lexicon/chatbot as a transparent first-line triage tool, but do not treat it as authoritative. Evaluate a trained model on a labelled, multilingual, time-separated test set before deployment; retain human escalation for health/safety complaints.

At 15-minute intervals, 100 new stations generate 100 × 96 = 9,600 new observations each day (about 3.50 million/year), before counting the existing stations. This makes incremental ingestion and database indexing more important than re-reading all CSV files for each question.
