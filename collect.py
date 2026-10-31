
import requests
import pandas as pd

# 1. Public Scaleway incident data API endpoint
url = "https://status.scaleway.com/api/v2/incidents.json"

# 2. Retrieve data from the API
response = requests.get(url, timeout=30)
response.raise_for_status()

# 3. Extract incident records from the API response
incidents = response.json()["incidents"]

# 4. Organise the required incident fields into a table
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

# 5. Export the data to a CSV file
df.to_csv("scaleway_incidents.csv", index=False)

print("Success!")
print("Number of incidents:", len(df))
print(df.head())
