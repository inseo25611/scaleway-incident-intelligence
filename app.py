import pandas as pd
import streamlit as st

st.set_page_config(page_title="Scaleway Incident Intelligence", page_icon="📊", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px;}
h1 {font-size: 2.5rem !important; font-weight: 750 !important; letter-spacing: -0.8px;}
div[data-testid="stMetric"] {background-color: rgba(128,128,128,.08); border: 1px solid rgba(128,128,128,.18); border-radius: 12px; padding: 18px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("incident_aggregates.csv")

df = load_data()
st.title("Scaleway Incident Intelligence")
st.caption("Independent analysis of aggregated public status information · Snapshot: 6–30 October 2026")
st.info("Exploratory analysis of a limited 50-record snapshot, not a measure of overall service reliability. Incident creation-to-resolution time is not service downtime. Individual incident records are not republished.")

st.sidebar.header("Filters")
category = st.sidebar.selectbox("Incident Category", ["All"] + sorted(df.category_clean.dropna().unique().tolist()))
impact = st.sidebar.selectbox("Impact Level", ["All"] + sorted(df.impact.dropna().unique().tolist()))
filtered = df.copy()
if category != "All":
    filtered = filtered[filtered.category_clean == category]
if impact != "All":
    filtered = filtered[filtered.impact == impact]

n = int(filtered.incidents.sum())
n_resolved = int(filtered.with_resolution.sum())
st.subheader("Portfolio Overview")
a, b, c = st.columns(3)
a.metric("Reported Incidents", n)
b.metric("With Resolution Timestamp", n_resolved)
if category == "All" and impact == "All":
    c.metric("Median Recorded Duration", "17.83 h")
else:
    c.metric("Median Recorded Duration", "—")
    st.caption("Median duration is shown for the overall snapshot only; filtered medians are not available in the published aggregate dataset.")

st.divider()
st.subheader("Key Findings")
st.caption("All findings below describe the original 50-record snapshot and do not change with filters.")
k1,k2,k3=st.columns(3)
k1.metric("Minor Impact Share", "82%")
k1.write("41 of 50 records were classified as minor.")
k2.metric("Generative API-related", "10")
k2.write("Ten titles matched different Generative API / GAPI labels after standardisation.")
k3.metric("Missing Resolution Timestamp", "8")
k3.write("Five records were identified and three were monitoring at capture time.")
st.warning("Recorded duration is not equivalent to actual downtime. Incident types and categories are heuristically classified.")

def weighted_counts(column):
    return filtered.groupby(column)["incidents"].sum().sort_values(ascending=False)

st.divider()
left,right=st.columns(2)
with left:
    st.subheader("Incidents by Impact")
    counts=weighted_counts("impact")
    if not counts.empty: st.bar_chart(counts)
    else: st.info("No matching incidents")
with right:
    st.subheader("Incidents by Category")
    counts=weighted_counts("category_clean").head(10)
    if not counts.empty: st.bar_chart(counts)
    else: st.info("No matching categories")
st.divider()
st.subheader("Incident Types")
counts=weighted_counts("incident_type")
if not counts.empty: st.bar_chart(counts)
else: st.info("No matching incident types")

st.divider()
st.subheader("About this dataset")
st.write("Only aggregated counts and classifications are published here. The source API may change over time; the 2026 snapshot is not refreshed automatically. No individual incident IDs, original titles, or timestamps are included in the deployment data.")
st.caption("Source: https://status.scaleway.com/ · Independent, non-commercial portfolio analysis. Not affiliated with, endorsed by, or maintained by Scaleway.")
