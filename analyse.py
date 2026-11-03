
import pandas as pd

# STEP 1: Load the saved CSV file
df = pd.read_csv("scaleway_incidents.csv")

# STEP 2: Check the number of records
print("=== DATA OVERVIEW ===")
print("Total incidents:", len(df))

# STEP 3: Count incidents by impact level
print("\n=== INCIDENTS BY IMPACT ===")
print(df["impact"].value_counts())

# STEP 4: Convert timestamps for calculations in Python
df["created_at"] = pd.to_datetime(
    df["created_at"], utc=True
)

df["resolved_at"] = pd.to_datetime(
    df["resolved_at"], utc=True
)

# STEP 5: Calculate duration from incident creation to resolution
df["duration_hours"] = (
    df["resolved_at"] - df["created_at"]
).dt.total_seconds() / 3600

# STEP 6: Select resolved incidents
resolved = df[
    df["resolved_at"].notna()
    & (df["duration_hours"] >= 0)
]

print("\n=== RESOLUTION TIME ===")
print("Resolved incidents:", len(resolved))

if len(resolved) > 0:
    print(
        "Median duration (hours):",
        round(resolved["duration_hours"].median(), 2)
    )
    print(
        "Longest duration (hours):",
        round(resolved["duration_hours"].max(), 2)
    )

# STEP 7: Save the results
df.to_csv("scaleway_analysed.csv", index=False)


# Identify the five incidents with the longest recorded durations
print("\n=== TOP 5 LONGEST INCIDENTS ===")

top5 = resolved.sort_values(
    by="duration_hours",
    ascending=False
).head(5)

for _, row in top5.iterrows():
    print("---------------------------")
    print("Name:", row["name"])
    print("Impact:", row["impact"])
    print("Created:", row["created_at"])
    print("Resolved:", row["resolved_at"])
    print("Duration:", round(row["duration_hours"], 2), "hours")


# Extract service names from incident titles
import re

def extract_product(name):
    match = re.match(r"^\[([^\]]+)\]", str(name))

    if match:
        return match.group(1).strip()

    return "Unclassified"

df["product"] = df["name"].apply(extract_product)

print("\n=== INCIDENTS BY PRODUCT ===")
print(df["product"].value_counts())

# Save the CSV again with the added product classification
df.to_csv("scaleway_analysed.csv", index=False)

print("\nProduct classification completed!")


# Analyse recorded incident duration by service
print("\n=== DURATION BY SERVICE ===")

# Load analysed data including product classifications
service_df = pd.read_csv("scaleway_analysed.csv")

# Select records with available duration and product data
service_df = service_df.dropna(
    subset=["duration_hours", "product"]
)

# Exclude negative or invalid durations
service_df = service_df[
    service_df["duration_hours"] >= 0
]

# Aggregate duration metrics by service
summary = service_df.groupby("product").agg(
    incidents=("id", "count"),
    median_hours=("duration_hours", "median"),
    max_hours=("duration_hours", "max")
)

# Include services with at least two incident records
summary = summary[summary["incidents"] >= 2]

# Sort by median recorded duration in descending order
summary = summary.sort_values(
    "median_hours",
    ascending=False
)

# Round results to two decimal places
summary = summary.round(2)

print(summary.to_string())

# Export the results to a CSV file
summary.to_csv("service_duration_summary.csv")

print("\nService duration analysis completed!")

print("\nAnalysis completed!")




# STEP 21: Data Quality Check

print("\n=== DATA QUALITY CHECK ===")

# Reload the original CSV file
quality_df = pd.read_csv("scaleway_incidents.csv")

print("\n1. Total records:")
print(len(quality_df))

print("\n2. Duplicate incident IDs:")
print(quality_df["id"].duplicated().sum())

print("\n3. Missing values:")
print(quality_df.isna().sum())

print("\n4. Status of incidents without resolved_at:")

missing_resolution = quality_df[
    quality_df["resolved_at"].isna()
]

print(
    missing_resolution["status"].value_counts(
        dropna=False
    )
)

print("\n5. Incidents without resolution timestamps:")

print(
    missing_resolution[
        ["name", "status", "impact"]
    ].to_string(index=False)
)

print("\nData quality check completed!")


# STEP 23: Standardise incident categories

import pandas as pd

df = pd.read_csv("scaleway_analysed.csv")

def clean_category(value):
    name = str(value).strip()
    lower = name.lower()

    if lower in [
        "generative api",
        "generative apis",
        "generativeapi",
        "generative api's",
        "gapi"
    ]:
        return "Generative API"

    if lower == "cockpit":
        return "Cockpit"

    if lower in ["fr-par", "fr-par-1", "nl-ams"]:
        return "Region-labelled"

    return name

df["category_clean"] = df["product"].apply(
    clean_category
)

print("\n=== CLEANED CATEGORIES ===")
print(df["category_clean"].value_counts())

df.to_csv(
    "scaleway_analysed.csv",
    index=False
)

print("\nCategory cleaning completed!")



# STEP 25: Classify incident types

import pandas as pd

df = pd.read_csv("scaleway_analysed.csv")

def classify_incident(name):
    text = str(name).lower()

    if "timeout" in text or "timed out" in text:
        return "Timeout"

    if "5xx" in text or "503" in text or "500 error" in text:
        return "HTTP 5xx Error"

    if "latency" in text or "latencies" in text:
        return "Latency"

    if "ticket" in text or "call handling" in text:
        return "Support Delay"

    if "synchronization" in text or "synchronisation" in text:
        return "Synchronization"

    if "unreachable" in text or "unavailable" in text:
        return "Unavailability"

    return "Other / Review Needed"


df["incident_type"] = df["name"].apply(
    classify_incident
)

print("\n=== INCIDENT TYPES ===")
print(df["incident_type"].value_counts())

print("\n=== INCIDENTS NEEDING REVIEW ===")
print(
    df.loc[
        df["incident_type"] == "Other / Review Needed",
        ["name", "category_clean"]
    ].to_string(index=False)
)

df.to_csv("scaleway_analysed.csv", index=False)

print("\nIncident classification completed!")

