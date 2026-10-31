
import pandas as pd

# STEP 1: 저장한 CSV 파일 열기
df = pd.read_csv("scaleway_incidents.csv")

# STEP 2: 데이터가 몇 줄인지 확인
print("=== DATA OVERVIEW ===")
print("Total incidents:", len(df))

# STEP 3: 장애 영향 수준별 건수
print("\n=== INCIDENTS BY IMPACT ===")
print(df["impact"].value_counts())

# STEP 4: 날짜를 Python이 계산할 수 있게 변환
df["created_at"] = pd.to_datetime(
    df["created_at"], utc=True
)

df["resolved_at"] = pd.to_datetime(
    df["resolved_at"], utc=True
)

# STEP 5: 기록 생성부터 해결까지 걸린 시간 계산
df["duration_hours"] = (
    df["resolved_at"] - df["created_at"]
).dt.total_seconds() / 3600

# STEP 6: 해결된 장애만 선택
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

# STEP 7: 결과 저장
df.to_csv("scaleway_analysed.csv", index=False)


# 가장 오래 걸린 장애 5건 확인
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


# 장애 제목에서 제품 이름 추출하기
import re

def extract_product(name):
    match = re.match(r"^\[([^\]]+)\]", str(name))

    if match:
        return match.group(1).strip()

    return "Unclassified"

df["product"] = df["name"].apply(extract_product)

print("\n=== INCIDENTS BY PRODUCT ===")
print(df["product"].value_counts())

# 제품 정보가 추가된 CSV 다시 저장
df.to_csv("scaleway_analysed.csv", index=False)

print("\nProduct classification completed!")


# 서비스별 기록상 해결시간 분석
print("\n=== DURATION BY SERVICE ===")

# 분석된 CSV에서 제품 분류까지 포함된 데이터 불러오기
service_df = pd.read_csv("scaleway_analysed.csv")

# 해결시간이 있는 기록만 선택
service_df = service_df.dropna(
    subset=["duration_hours", "product"]
)

# 음수나 잘못된 해결시간 제외
service_df = service_df[
    service_df["duration_hours"] >= 0
]

# 서비스별로 묶어서 계산
summary = service_df.groupby("product").agg(
    incidents=("id", "count"),
    median_hours=("duration_hours", "median"),
    max_hours=("duration_hours", "max")
)

# 기록이 최소 2건 있는 서비스만 선택
summary = summary[summary["incidents"] >= 2]

# 중앙값이 긴 순서로 정렬
summary = summary.sort_values(
    "median_hours",
    ascending=False
)

# 소수점 둘째 자리까지 표시
summary = summary.round(2)

print(summary.to_string())

# 결과를 CSV 파일로 저장
summary.to_csv("service_duration_summary.csv")

print("\nService duration analysis completed!")

print("\nAnalysis completed!")




# STEP 21: Data Quality Check

print("\n=== DATA QUALITY CHECK ===")

# 원본 CSV를 다시 불러오기
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
