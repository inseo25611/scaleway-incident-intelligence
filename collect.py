
import requests
import pandas as pd

# 1. Scaleway의 공개 장애 데이터 주소
url = "https://status.scaleway.com/api/v2/incidents.json"

# 2. 인터넷에서 데이터 가져오기
response = requests.get(url, timeout=30)
response.raise_for_status()

# 3. 장애 기록만 꺼내기
incidents = response.json()["incidents"]

# 4. 필요한 정보만 표로 정리하기
rows = []

for incident in incidents:
    rows.append({
        "id": incident["id"],
        "name": incident["name"],
        "status": incident["status"],
        "impact": incident["impact"],
        "created_at": incident["created_at"],
        "resolved_at": incident.get("resolved_at"),
    })

df = pd.DataFrame(rows)

# 5. CSV 파일로 저장하기
df.to_csv("scaleway_incidents.csv", index=False)

print("Success!")
print("Number of incidents:", len(df))
print(df.head())
