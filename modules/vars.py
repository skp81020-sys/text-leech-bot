import os

API_ID    = os.environ.get("API_ID", "")
API_HASH  = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

WEBHOOK = True  # Don't change this
PORT = int(os.environ.get("PORT", 8870))  # Default to 8870 if not set

# ==================== CLASSPLUS MULTIPLE TOKENS ====================
# Add multiple tokens here comma separated to avoid 403 errors
# Format: "token1,token2,token3"
# Or use environment variable: CLASSPLUS_TOKENS

CLASSPLUS_TOKENS = os.environ.get("CLASSPLUS_TOKENS", 
    # Default token (replace with your actual tokens)
    "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0,"
    # Add more tokens here (make sure to end with quote)
).split(",")

# Remove empty tokens and strip whitespace
CLASSPLUS_TOKENS = [token.strip() for token in CLASSPLUS_TOKENS if token.strip()]

print(f"✅ Loaded {len(CLASSPLUS_TOKENS)} ClassPlus token(s)")
