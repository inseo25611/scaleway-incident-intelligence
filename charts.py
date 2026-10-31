
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scaleway_analysed.csv")

# Arrange impact levels in the desired order
order = ["critical", "major", "minor", "none"]

counts = df["impact"].value_counts()
counts = counts.reindex(order, fill_value=0)

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(counts.index, counts.values)

# Display incident counts above the bars
ax.bar_label(bars, padding=3)

ax.set_title("Scaleway: Reported Incidents by Impact")
ax.set_xlabel("Impact Level")
ax.set_ylabel("Number of Incidents")
ax.set_ylim(0, counts.max() * 1.15)

plt.tight_layout()
plt.savefig("incidents_by_impact.png", dpi=150)
plt.show()

print("Updated graph saved!")


# Top 10 incident categories by number of incidents
df = pd.read_csv("scaleway_analysed.csv")

product_counts = df["product"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.barh(
    product_counts.index,
    product_counts.values
)

ax.bar_label(bars, padding=3)

ax.set_title("Scaleway: Top 10 Incident Categories")
ax.set_xlabel("Number of Reported Incidents")
ax.set_ylabel("Category")

# Display the most frequent categories at the top
ax.invert_yaxis()

# Add horizontal space to prevent value labels from being cut off
ax.set_xlim(0, product_counts.max() * 1.2)

plt.tight_layout()

plt.savefig("incidents_by_product.png", dpi=150)
plt.show()

print("Product chart created successfully!")


# Chart of recorded incident duration by service
summary = pd.read_csv("service_duration_summary.csv")

if summary.empty:
    print("Not enough data to create this chart.")
else:
    # Top 10 services with the longest median recorded durations
    top10 = summary.nlargest(10, "median_hours")

    fig, ax = plt.subplots(figsize=(11, 6))

    bars = ax.barh(
        top10["product"],
        top10["median_hours"]
    )

    ax.bar_label(bars, fmt="%.1f", padding=3)

    ax.invert_yaxis()

    ax.set_title(
        "Scaleway: Median Reported Incident Duration"
    )
    ax.set_xlabel("Hours")
    ax.set_ylabel("Incident Category")
    ax.set_xlim(0, top10["median_hours"].max() * 1.2)

    plt.tight_layout()

    plt.savefig(
        "duration_by_service.png",
        dpi=150
    )

    plt.show()

    print("Duration chart created successfully!")



# Cleaned incident categories chart

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scaleway_analysed.csv")

counts = (
    df["category_clean"]
    .value_counts()
    .head(10)
)

fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.barh(counts.index, counts.values)

ax.bar_label(bars, padding=3)
ax.invert_yaxis()

ax.set_title(
    "Scaleway: Top 10 Incident Categories (Cleaned)"
)
ax.set_xlabel("Number of Reported Incidents")
ax.set_xlim(0, counts.max() * 1.2)

plt.tight_layout()

plt.savefig(
    "incidents_by_category_cleaned.png",
    dpi=150
)

plt.show()

print("Cleaned category chart created!")



# STEP 26: Incident type chart

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scaleway_analysed.csv")

counts = df["incident_type"].value_counts()

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.barh(counts.index, counts.values)

ax.bar_label(bars, padding=3)
ax.invert_yaxis()

ax.set_title("Scaleway: Reported Incident Types")
ax.set_xlabel("Number of Incidents")
ax.set_xlim(0, counts.max() * 1.2)

plt.tight_layout()

plt.savefig("incidents_by_type.png", dpi=150)
plt.show()

print("Incident type chart created!")

plt.savefig("incidents_by_type.png", dpi=150)
plt.show()

print("Incident type chart created!")
