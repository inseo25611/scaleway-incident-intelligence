# Scaleway Incident Intelligence

An **independent, non-commercial portfolio project** analysing reported cloud-service incidents from the publicly accessible [Scaleway Status API](https://status.scaleway.com/api).

[View the Streamlit dashboard](https://scaleway-incident-intelligence.streamlit.app/)

## Overview

A limited snapshot of 50 incident records (created 6–30 October 2026) was collected and analysed locally using Python and pandas. The public dashboard uses **aggregated counts only**, with filters by standardised category and reported impact.

## Findings for the original 50-record snapshot

- 41 / 50 incidents (82%) had a reported `minor` impact.
- 10 records were classified as Generative API-related after normalising varying title labels.
- 42 records had resolution timestamps; the median recorded creation-to-resolution duration was **17.83 hours**.
- 8 records lacked a resolution timestamp (5 `identified`, 3 `monitoring` at collection time).

The metrics are descriptive observations of this snapshot, not verified root causes, measured customer impact, actual downtime or Scaleway-wide reliability estimates.

## Dashboard features

- Category and impact filters
- Aggregated incident-count KPIs and charts
- Keyword-based incident-type categories
- Non-filtered median duration for the original 50-record snapshot

The original incident-by-incident table and incident-level CSV download have been removed from this public version.

## Run the published dashboard locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Reproduce the analysis privately (optional)

Run `python collect.py` to retrieve the API's **current** incident set, then `python analyse.py` to perform local analysis. These scripts create local incident-level CSV files that are excluded by `.gitignore`. Do not commit them to the public repository. Because the API changes over time, running the scripts later will not recreate the same October 2026 snapshot.

`charts.py` is an optional local visualisation script, not required to run the public app. The generated `service_duration_summary.csv` is also ignored.

## Data handling

- Published dataset: `incident_aggregates.csv` (category, impact, type, status, counts)
- Not published: incident IDs, original titles, row-level timestamps, raw API CSV, processed row-level CSV
- The Streamlit app does not offer incident-level detail or data downloads.
- This is a precautionary publication approach, **not a statement that Scaleway has granted a reuse licence**. Any broader redistribution should be confirmed with the rightsholder.

## Limitations and disclaimer

Service categories are inferred from incident titles, including heuristic label normalisation. Incident types are keyword-classified, not independently verified. The snapshot is limited to 50 records. Recorded creation-to-resolution duration must not be interpreted as actual service downtime. Findings should not be construed as an assessment of Scaleway's overall service reliability.

This independent project is not affiliated with, endorsed by, or maintained by Scaleway. Scaleway names and marks belong to their respective owners.
