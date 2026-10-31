
# Scaleway Incident Intelligence

An independent cloud operations analytics project using publicly available Scaleway status data.

## Project Overview

This project explores reported cloud service incidents to identify patterns in incident frequency, impact classification, recorded resolution duration, and service categories.

The goal is to turn publicly available operational data into an interactive decision-support dashboard.

## Dataset

- Source: Public Scaleway Status API
- Sample: 50 recent incident records
- Records with resolution timestamps: 42
- Collection: October 2026

The dataset is a limited snapshot, not the complete incident history.

## Key Findings

- 82% of incidents were classified as minor.
- 10 records were identified as Generative API-related after standardising title labels.
- 8 records had no resolution timestamp: 5 identified and 3 monitoring.
- The median recorded incident duration among the 42 records with resolution timestamps was 17.83 hours.

## Dashboard Features

- Interactive category and impact filters
- Incident frequency and severity visualisations
- Recorded incident duration metrics
- Keyword-based incident type classification
- Detailed incident records
- Filtered CSV export

## Technology

Python, Pandas, Streamlit, Matplotlib, Requests

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```

## Limitations

Incident duration is calculated from creation to recorded resolution and must not be interpreted as actual service downtime.

Service categories are derived from incident titles and standardised using heuristic rules. Incident types are classified using keywords, not verified root-cause analysis.

Findings are exploratory and should not be interpreted as an assessment of Scaleway's overall service reliability.

## Disclaimer

This is an independent portfolio project and is not affiliated with or endorsed by Scaleway.
