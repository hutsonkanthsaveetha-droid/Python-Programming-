# A2 - Cleaning, normalisation and formatting design

| Problem | Rule | Reason |
|---|---|---|
| Blank / `NA` numeric values | Convert to missing; fill using station-specific median, then global median if no station value exists | Median is robust to pollution spikes; missingness remains counted in the cleaning log |
| Negative or impossible PM2.5/PM10/NO2 | Treat as invalid/missing when outside PM2.5 0-999, PM10 0-2000, NO2 0-1000 | Sensor faults must not become real readings |
| Temperature in Fahrenheit | Convert using `(F - 32) * 5 / 9` before validation | All stored values must use Celsius |
| Duplicate station/date/hour | Keep first valid key and log later duplicates | One station cannot have two observations for the same hour |
| Malformed date/hour | Reject and record file/line/reason | Invalid keys cannot be grouped or indexed safely |

## Normalisation
Min-max: `x' = (x - min(x)) / (max(x) - min(x))`; maps values to [0,1] and is useful when a bounded scale is needed. If max equals min, return 0 for each value to avoid division by zero. Z-score: `z = (x - mean(x)) / population_standard_deviation(x)`; useful when comparing deviations from the mean and retaining outlier distance. If standard deviation is zero, return 0. Fit parameters must be computed on the training/reference period and reused for later comparisons.

## Standard formats
Station names are trimmed and title-cased; dates use ISO `YYYY-MM-DD`; hours are integers 0-23; measurements are numeric values rounded to two decimals; temperature is stored only in Celsius; missing/invalid decisions are recorded separately.

## Alternative: drop missing values
Dropping missing values is O(n) and O(1) extra streaming space, but it can bias daily averages if sensor loss occurs during high-pollution periods and reduces valid sample counts. Forward fill is O(n) streaming. Median by sorting is O(n log n) time and O(n) storage (or O(n) selection-based expected time). The project uses station medians for robust repair and preserves rejected/filled counts for traceability.
