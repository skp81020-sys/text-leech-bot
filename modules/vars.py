import os

API_ID    = os.environ.get("API_ID", "")
API_HASH  = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

WEBHOOK = True  
PORT = int(os.environ.get("PORT", 8870))  

# ==================== CLASSPLUS CONFIGURATION ====================
# Multiple tokens comma separated - Bot will rotate automatically
CLASSPLUS_TOKENS = os.environ.get("CLASSPLUS_TOKENS", 
    # Yahan apne tokens add karo (comma separated if multiple)
    "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTYxMTE2NDcxLCJvcmdJZCI6NjI3MTc3LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTk1MDQ5MzczMDkiLCJuYW1lIjoiU2F0aXNoIEt1bWFyIiwiZW1haWwiOm51bGwsImlzSW50ZXJuYXRpb25hbCI6MCwiZGVmYXVsdExhbmd1YWdlIjoiRU4iLCJjb3VudHJ5Q29kZSI6IklOIiwiY291bnRyeUlTTyI6IjkxIiwidGltZXpvbmUiOiJHTVQrNTozMCIsImlzRGl5Ijp0cnVlLCJvcmdDb2RlIjoiamZxcnhjIiwiaXNEaXlTdWJhZG1pbiI6MCwiZmluZ2VycHJpbnRJZCI6IjhkMThhYTlkY2RkYzRiY2FiMGU1N2FlZjMyNzdmNjRjIiwiaWF0IjoxNzY5ODg5NjYzLCJleHAiOjE3NzA0OTQ0NjN9.8DDauOaXrG-mwK1qUQDgwqVE-6aMBLYLbQv6i5N5y7bC5SajqSjHPzt8UJUqbZ8a"
).split(",")

# Clean tokens
CLASSPLUS_TOKENS = [token.strip() for token in CLASSPLUS_TOKENS if token.strip()]
if not CLASSPLUS_TOKENS:
    print("⚠️  WARNING: No ClassPlus tokens configured!")
else:
    print(f"✅ Loaded {len(CLASSPLUS_TOKENS)} ClassPlus token(s)")
