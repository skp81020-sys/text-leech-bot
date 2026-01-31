 import time
import math
import os
import random
import requests
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


# ==================== NEW CODE FOR CLASSPLUS TOKEN MANAGEMENT ====================

class TokenManager:
    """Manages multiple ClassPlus tokens with rotation to avoid 403 errors"""
    def __init__(self, tokens):
        if isinstance(tokens, str):
            self.tokens = [t.strip() for t in tokens.split(",") if t.strip()]
        else:
            self.tokens = [t.strip() for t in tokens if t.strip()]
        self.current_index = 0
        self.failed_tokens = set()
        print(f"📝 TokenManager initialized with {len(self.tokens)} tokens")
    
    def get_current_token(self):
        """Get current active token"""
        if not self.tokens:
            return None
        return self.tokens[self.current_index % len(self.tokens)]
    
    def get_next_token(self):
        """Rotate to next token"""
        if not self.tokens:
            return None
        self.current_index = (self.current_index + 1) % len(self.tokens)
        token = self.tokens[self.current_index]
        print(f"🔄 Switched to token {self.current_index + 1}/{len(self.tokens)}")
        return token
    
    def mark_failed(self, token):
        """Mark a token as failed"""
        if token:
            self.failed_tokens.add(token)
            print(f"❌ Token marked failed: {token[:25]}...")
            
        # If all tokens failed, reset and try again
        if len(self.failed_tokens) >= len(self.tokens):
            print("⚠️ All tokens failed! Clearing failed list and retrying...")
            self.failed_tokens.clear()

def get_random_headers():
    """Generate random browser headers to avoid detection"""
    user_agents = [
        "Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://web.classplusapp.com',
        'Referer': 'https://web.classplusapp.com/',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

def get_classplus_signed_url(video_url, token_manager, max_retries=3):
    """
    Resolve ClassPlus video URL using token rotation
    Returns: Direct playable URL or raises Exception
    """
    api_url = f"https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={video_url}"
    
    for attempt in range(max_retries):
        token = token_manager.get_current_token()
        if not token:
            raise Exception("No ClassPlus tokens available! Set CLASSPLUS_TOKENS in vars.py")
        
        headers = {
            **get_random_headers(),
            'x-access-token': token,
            'authority': 'api.classplusapp.com',
            'api-version': '8'
        }
        
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_retries} resolving URL...")
            response = requests.get(api_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'url' in data and data['url']:
                    print(f"✅ URL resolved successfully!")
                    return data['url']
                else:
                    error_msg = data.get('message', 'Empty response from API')
                    print(f"⚠️ API Response: {error_msg}")
                    token_manager.mark_failed(token)
                    
            elif response.status_code == 403:
                print(f"❌ 403 Forbidden (Token {token_manager.current_index + 1} expired)")
                token_manager.mark_failed(token)
                token_manager.get_next_token()
                time.sleep(2)
                
            elif response.status_code == 401:
                print(f"❌ 401 Unauthorized (Token {token_manager.current_index + 1} invalid)")
                token_manager.mark_failed(token)
                token_manager.get_next_token()
                
            else:
                print(f"⚠️ HTTP {response.status_code}: {response.text[:200]}")
                token_manager.get_next_token()
                
        except requests.exceptions.Timeout:
            print(f"⏱️ Request timeout, switching token...")
            token_manager.get_next_token()
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}")
            token_manager.get_next_token()
            time.sleep(1)
    
    raise Exception(f"Failed after {max_retries} attempts. All ClassPlus tokens exhausted.")


# ==================== EXISTING YOUR CODE (UNCHANGED) ====================

def hrb(value, digits=2, delim="", postfix=""):
    """Return a human-readable file size.
    """
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix

def hrt(seconds, precision=0):
    """Return a human-readable time delta as a string.
    """
    pieces = []
    value = timedelta(seconds=seconds)
    
    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


timer = Timer()

# Powered By Ankush
async def progress_bar(current, total, reply, start):
    if timer.can_send():
        now = time.time()
        diff = now - start
        if diff < 1:
            return
        else:
            perc = f"{current * 100 / total:.1f}%"
            elapsed_time = round(diff)
            speed = current / elapsed_time
            remaining_bytes = total - current
            if speed > 0:
                eta_seconds = remaining_bytes / speed
                eta = hrt(eta_seconds, precision=1)
            else:
                eta = "-"
            sp = str(hrb(speed)) + "/s"
            tot = hrb(total)
            cur = hrb(current)
            bar_length = 11
            completed_length = int(current * bar_length / total)
            remaining_length = bar_length - completed_length
            progress_bar = "◆" * completed_length + "◇" * remaining_length
            
            try:
                await reply.edit(f'\n**╭─⌯══⟰ 𝐔𝐩𝐥𝐨𝐝𝐢𝐧𝐠 ⟰══⌯──★ \n├⚡ {progress_bar}|﹝{perc}﹞ \n├🚀 Speed » {sp} \n├📟 Processed » {cur}\n├🧲 Size - ETA » {tot} - {eta} \n╰─══ ✪  𝗔𝘀𝗵𝘂𝘁𝗼𝘀𝗵 𝗚𝗼𝘀𝘄𝗮𝗺𝗶 𝟮𝟰 ✪ ══─★**\n') 
            except FloodWait as e:
                time.sleep(e.x)
