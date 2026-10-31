
import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Scaleway Incident Intelligence",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>
    /* Main content width and spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Main title */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.8px;
    }

    /* Section headings */
    h3 {
        font-weight: 650 !important;
        margin-top: 0.5rem;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 12px;
        padding: 18px;
    }

    /* Metric values */
    div[data-testid="stMetricValue"] {
        font-size: 1.9rem;
        font-weight: 700;
    }

    /* Sidebar spacing */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)



# ==========================================
# 2. LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_csv("scaleway_analysed.csv")

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        utc=True,
        format="mixed"
    )

    df["resolved_at"] = pd.to_datetime(
        df["resolved_at"],
        utc=True,
        format="mixed"
    )

    return df


df = load_data()


# ==========================================
# 3. HEADER
# ==========================================

st.title("Scaleway Incident Intelligence")

st.caption(
    "Independent analysis of public Scaleway status records"
)

st.info(
    "This dashboard analyses a snapshot of 50 recent "
    "publicly reported incidents, not Scaleway's complete "
    "incident history. Recorded duration is measured "
    "from incident creation to its resolution timestamp, "
    "not actual service downtime."
)


# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filters")

# Category filter
categories = sorted(
    df["category_clean"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Incident Category",
    ["All"] + categories,
    index=0
)

# Impact filter
impacts = sorted(
    df["impact"].dropna().unique().tolist()
)

selected_impact = st.sidebar.selectbox(
    "Impact Level",
    ["All"] + impacts,
    index=0
)


# ==========================================
# 5. APPLY FILTERS
# ==========================================

filtered = df.copy()

if selected_category != "All":

    filtered = filtered[
        filtered["category_clean"] == selected_category
    ]

if selected_impact != "All":

    filtered = filtered[
        filtered["impact"] == selected_impact
    ]


# ==========================================
# 6. OVERVIEW METRICS
# ==========================================

st.subheader("Portfolio Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Reported Incidents",
    len(filtered)
)

resolved = filtered[
    filtered["resolved_at"].notna()
    & filtered["duration_hours"].notna()
    & (filtered["duration_hours"] >= 0)
].copy()

col2.metric(
    "With Resolution Timestamp",
    len(resolved)
)

median_duration = resolved["duration_hours"].median()

col3.metric(
    "Median Recorded Duration",
    f"{median_duration:.2f} h"
    if pd.notna(median_duration)
    else "N/A"
)


# ==========================================
# KEY FINDINGS
# ==========================================

st.divider()
st.subheader("Key Findings")

st.caption(
    "Findings below describe the full 50-record snapshot "
    "and do not change with sidebar filters."
)

k1, k2, k3 = st.columns(3)

with k1:
    st.metric("Minor Impact Share", "82%")
    st.write(
        "41 of 50 reported incidents were "
        "classified as minor."
    )

with k2:
    st.metric("Generative API-related", "10")
    st.write(
        "Ten incident titles used variants of "
        "Generative API or GAPI."
    )

with k3:
    st.metric("Missing Resolution Timestamp", "8")
    st.write(
        "Five incidents were identified and "
        "three were monitoring."
    )

st.warning(
    "Interpretation: Reported incident duration is "
    "not equivalent to actual downtime. "
    "The sample contains only 50 recent records."
)


# ==========================================
# 7. CHARTS
# ==========================================

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("Incidents by Impact")

    impact_counts = (
        filtered["impact"]
        .value_counts()
        .rename_axis("Impact")
        .rename("Incidents")
    )

    if not impact_counts.empty:
        st.bar_chart(impact_counts)
    else:
        st.info("No incidents match the selected filters.")


with right:

    st.subheader("Incidents by Category")

    category_counts = (
        filtered["category_clean"]
        .value_counts()
        .head(10)
        .rename_axis("Category")
        .rename("Incidents")
    )

    if not category_counts.empty:
        st.bar_chart(category_counts)
    else:
        st.info("No category data available.")


# ==========================================
# 8. INCIDENT TYPES
# ==========================================

st.divider()

st.subheader("Incident Types")

type_counts = (
    filtered["incident_type"]
    .value_counts()
    .rename_axis("Incident Type")
    .rename("Incidents")
)

if not type_counts.empty:
    st.bar_chart(type_counts)
else:
    st.info("No incident type data available.")


# ==========================================
# 9. INCIDENT DETAILS
# ==========================================

st.divider()

st.subheader("Incident Details")

display_columns = [
    "name",
    "category_clean",
    "incident_type",
    "impact",
    "status",
    "created_at",
    "resolved_at",
    "duration_hours"
]

if not filtered.empty:

    display_df = filtered[
        display_columns
    ].sort_values(
        "created_at",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No incidents match the selected filters. "
        "Try selecting All."
    )


# ==========================================
# 10. DOWNLOAD DATA
# ==========================================

st.divider()

st.download_button(
    label="Download Filtered Data",
    data=filtered.to_csv(index=False),
    file_name="scaleway_filtered_incidents.csv",
    mime="text/csv"
)


# ==========================================
# 11. FOOTER
# ==========================================

st.caption(
    "Data source: Public Scaleway Status API. "
    "Independent portfolio project, "
    "not affiliated with Scaleway."
)
