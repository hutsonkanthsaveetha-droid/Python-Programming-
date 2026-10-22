# Task 12 — Design challenge

**Decision: MODIFY, not fully redesign.** The original modular design remains useful, but the rate card must become configurable by season, the fat step value changes seasonally, analyser readings can have two decimal places, and a bonus applies only when the ten-day supply is strictly greater than 500 L.

The code in `Task12/seasonal_demo.py` passes seasonal values as parameters. It rounds the analyser reading's difference to the nearest 0.1 percentage-point step using Decimal and ROUND_HALF_UP. Two decimal places in the reading do not mean that each 0.01% becomes a separate rate step: the given rule still describes 0.1% steps, so the nearest-step policy must be confirmed with the co-operative. Bonus is ₹0.50 per litre for a farmer whose ten-day total exceeds 500 L; exactly 500 L does not qualify.

Assumption: July–March uses the original rates because only April–June rates were supplied. Confirm whether seasonal SNF adjustment remains ₹0.30 and whether the bonus is applied to every litre supplied during the ten-day period. The demo applies the bonus to the current payment quantity when `ten_day_litres > 500`. In a production system, accumulate and verify the ten-day quantity before finalising bonus payments.

Run `python -m Task12.seasonal_demo` and record actual output. Include both seasons and the 500/501/600 L threshold tests in the report.
