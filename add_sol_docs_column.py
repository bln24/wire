#!/usr/bin/env python3
"""Add SolicitationDocs and DocumentUrl columns to WIREPipeline SP list."""
import json, requests

with open("/Users/t24/Desktop/T24/config/integrations.json") as f:
    cfg = json.load(f)

CLIENT_ID = cfg["clientId"]
CLIENT_SECRET = cfg["clientSecret"]
TENANT_ID = cfg["tenantId"]
SP_SITE = cfg["sharepoint"]["wirePipelineSiteId"]
SP_LIST = cfg["sharepoint"]["wirePipelineListId"]

# Get app token
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
tok_resp = requests.post(token_url, data={
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://graph.microsoft.com/.default"
})
tok_resp.raise_for_status()
token = tok_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

base = f"https://graph.microsoft.com/v1.0/sites/{SP_SITE}/lists/{SP_LIST}/columns"

# Check existing columns
existing = requests.get(base, headers=headers)
existing.raise_for_status()
col_names = [c.get("name","") for c in existing.json().get("value",[])]
print(f"Existing columns: {len(col_names)}")

for col_name in ["SolicitationDocs", "DocumentUrl"]:
    if col_name in col_names:
        print(f"  {col_name} already exists, skipping")
        continue
    body = {"name": col_name, "text": {"allowMultipleLines": True, "maxLength": 10000}}
    r = requests.post(base, headers=headers, json=body)
    if r.status_code in (200, 201):
        print(f"  {col_name} created OK")
    else:
        print(f"  {col_name} failed: {r.status_code} {r.text[:200]}")

print("Done.")
