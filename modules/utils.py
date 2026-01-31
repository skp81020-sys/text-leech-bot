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

# ==================== CLASSPLUS TOKEN MANAGER ====================

class TokenManager:
    """Advanced Token Manager with rotation and failure tracking"""
    def __init__(self, tokens):
        if isinstance(tokens, str):
            self.tokens = [t.strip() for t in tokens.split(",") if t.strip()]
        else:
            self.tokens = [t.strip() for t in tokens if t.strip()]
        
        self.current_index = 0
        self.failed_tokens = {}
        print(f"📝 TokenManager initialized with {len(self.tokens)} tokens")
    
    def get_current_token(self):
        if not self.tokens:
            return None
        return self.tokens[self.current_index % len(self.tokens)]
    
    def get_next_token(self):
        if not self.tokens:
            return None
        self.current_index = (self.current_index + 1) % len(self.tokens)
        print(f"🔄 Switched to Token {self.current_index + 1}/{len(self.tokens)}")
        return self.tokens[self.current_index]
    
    def mark_failed(self, token, error_code="403"):
        if token not in self.failed_tokens:
            self.failed_tokens[token] = 0
        self.failed_tokens[token] += 1
        
        print(f"❌ Token {self.current_index + 1} failed (Code: {error_code})")
        
        if len(self.failed_tokens) >= len(self.tokens):
            print("⚠️  All tokens expired! Need fresh tokens.")
            return "ALL_EXPIRED"
        return "RETRY"

def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://web.classplusapp.com',
        'Referer': 'https://web.classplusapp.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Cache-Control': 'no-cache'
    }

def resolve_classplus_url(video_url, token_manager, max_retries=3):
    """Resolve ClassPlus encrypted URL to playable m3u8"""
    if '.m3u8' in video_url or '.mp4' in video_url:
        return video_url
    
    api_url = f"https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={video_url}"
    
    for attempt in range(max_retries):
        token = token_manager.get_current_token()
        if not token:
            raise Exception("No tokens available!")
        
        headers = {
            **get_random_headers(),
            'x-access-token': token,
            'authority': 'api.classplusapp.com',
            'api-version': '8'
        }
        
        try:
            resp = requests.get(api_url, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('url'):
                    print(f"✅ URL resolved: {data['url'][:60]}...")
                    return data['url']
                    
            elif resp.status_code in [403, 401]:
                result = token_manager.mark_failed(token, str(resp.status_code))
                if result == "ALL_EXPIRED":
                    raise Exception("All tokens expired! Get fresh tokens.")
                token_manager.get_next_token()
                time.sleep(2)
            else:
                token_manager.get_next_token()
                time.sleep(1)
                
        except requests.exceptions.Timeout:
            token_manager.get_next_token()
        except Exception as e:
            print(f"❌ Error: {e}")
            token_manager.get_next_token()
    
    raise Exception(f"Failed after {max_retries} attempts.")

def hrb(value, digits=2, delim="", postfix=""):
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
    return "".join(pieces) if not precision else "".join(pieces[:precision])

timer = Timer()

async def progress_bar(current, total, reply, start):
    if timer.can_send():
        now = time.time()
        diff = now - start
        if diff < 1:
            return
        perc = f"{current * 100 / total:.1f}%"
        speed = current / diff if diff > 0 else 0
        remaining = total - current
        eta = hrt(remaining / speed, 1) if speed > 0 else "-"
        sp = hrb(speed) + "/s"
        tot = hrb(total)
        cur = hrb(current)
        bar = "◆" * int(current * 11 / total) + "◇" * (11 - int(current * 11 / total))
        
        try:
            await reply.edit(
                f'**╭─⌯══⟰ 𝐔𝐩𝐥𝐨𝐝𝐢𝐧𝐠 ⟰══⌯──★**\n'
                f'├⚡ {bar}|﹝{perc}﹞ \n'
                f'├🚀 {sp} | 📟 {cur}\n'
                f'├🧲 {tot} - ⏱️ {eta}\n'
                f'╰─══ ✪ 𝗔𝘀𝗵𝘂𝘁𝗼𝘀𝗵 𝗚𝗼𝘀𝘄𝗮𝗺𝗶 𝟮𝟰 ✪ ══─★'
            ) 
        except FloodWait as e:
            time.sleep(e.x)
