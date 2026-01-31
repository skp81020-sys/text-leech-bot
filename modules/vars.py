import os

API_ID    = os.environ.get("API_ID", "")
API_HASH  = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

WEBHOOK = True  
PORT = int(os.environ.get("PORT", 8870))  

# 👇👇 NAYA TOKEN (Org ID: 9183) 👇👇
CLASSPLUS_TOKENS = os.environ.get("CLASSPLUS_TOKENS", 
    "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTU1Njk1MTI4LCJvcmdJZCI6OTE4MywidHlwZSI6MSwibW9iaWxlIjoiOTE5NTA0OTM3MzA5IiwibmFtZSI6InNhdGlzaCBLdW1hciIsImVtYWlsIjoic2twODEwMjBAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOnRydWUsIm9yZ0NvZGUiOiJpcXZxbiIsImlzRGl5U3ViYWRtaW4iOjAsImZpbmdlcnByaW50SWQiOiIxZmVmOTZmZTkzN2U0N2MwOWNlYzc3MTgyZDE4N2M2YyIsImlhdCI6MTc2OTg5MDYwOSwiZXhwIjoxNzcwNDk1NDA5fQ.CWy4R1JMi-aqdQ9_JKkr1OXUCM6Iv-X1I8oR_zEzM5HQ9NUMYPYLlFtw_2CS6EkO"
).split(",")

CLASSPLUS_TOKENS = [token.strip() for token in CLASSPLUS_TOKENS if token.strip()]
print(f"✅ Loaded {len(CLASSPLUS_TOKENS)} token(s) for Org: 9183")
