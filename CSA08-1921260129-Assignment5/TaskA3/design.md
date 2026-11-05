# A3 - Analysis and visualisation design

| Board question | Chart | Reason |
|---|---|---|
| PM2.5 trend through a month | Line chart | Shows chronological direction, peaks and changes |
| Compare stations | Bar chart | Makes station means easy to rank |
| Temperature versus PM2.5 | Scatter plot | Shows association, clusters and outliers without implying causation |
| Hours with worst air | Bar chart of hourly averages | Identifies recurring high-exposure hours; a box plot can additionally show hourly spread |

## Daily summary table
Group by `(station, day)` and calculate `MIN(pm25)`, `MAX(pm25)`, `AVG(pm25)` and `COUNT(pm25)`. Store/display columns `station, day, min_pm25, max_pm25, mean_pm25, valid_readings`. SQL `GROUP BY station_id, day` computes it near the data; a Python pass can also maintain one min, max, sum and count per station/day. Both are O(n) time. SQL can stream/group in the database; a Python dictionary uses O(number of station-day groups) extra memory.

## Alternative: Python loops
Read rows once and update a dictionary keyed by `(station, day)`. Each update is average O(1), giving O(n) total time and O(g) space for g station-day groups. SQL `GROUP BY` is also O(n) expected scan time (plus grouping/index overhead) and keeps aggregation close to stored data, reducing data transfer to the application.
