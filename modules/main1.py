import os
import re
import sys
import asyncio
import requests
from utils import progress_bar, TokenManager, resolve_classplus_url
from vars import API_ID, API_HASH, BOT_TOKEN, WEBHOOK, PORT, CLASSPLUS_TOKENS
from pyromod import listen
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import core as helper

# Initialize
token_manager = TokenManager(CLASSPLUS_TOKENS) if CLASSPLUS_TOKENS else None
bot = Client("classplus_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Web Server
routes = web.RouteTableDef()
@routes.get("/")
async def root(request):
    return web.json_response({"status": "ClassPlus Bot", "tokens": len(CLASSPLUS_TOKENS)})

async def web_server():
    app = web.Application(client_max_size=30000000)
    app.add_routes(routes)
    return app

@bot.on_message(filters.command(["start"]))
async def start(bot, m):
    await m.reply_text(
        "**👋 ClassPlus Downloader**\n\nUse /upload to start downloading\n\n**Features:**\n✓ Multi-token rotation\n✓ Auto 403 retry\n✓ Skip thumbnails",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Start Upload", callback_data="upload")]
        ])
    )

@bot.on_message(filters.command(["upload"]))
async def upload(bot, m):
    if not token_manager:
        return await m.reply_text("❌ No tokens configured!")
    
    editable = await m.reply_text('📤 Send .txt file')
    input_msg = await bot.listen(editable.chat.id)
    
    try:
        x = await input_msg.download()
        await input_msg.delete()
        
        with open(x, "r") as f:
            content = f.read()
        links = [l.split("://", 1) for l in content.split("\n") if "://" in l and l.strip()]
        os.remove(x)
        
    except Exception as e:
        return await m.reply_text(f"❌ Error: {e}")
    
    await editable.edit(f"📋 {len(links)} links found\nStart from (default 1):")
    range_msg = await bot.listen(editable.chat.id)
    start = int(range_msg.text) if range_msg.text.isdigit() else 1
    await range_msg.delete()
    
    await editable.edit("Batch name:")
    name_msg = await bot.listen(editable.chat.id)
    batch = name_msg.text or "ClassPlus"
    await name_msg.delete()
    
    await editable.edit("Quality (144/240/360/480/720/1080):")
    q_msg = await bot.listen(editable.chat.id)
    quality = q_msg.text if q_msg.text.isdigit() else "480"
    await q_msg.delete()
    await editable.delete()
    
    # Process
    count = start
    for i in range(start-1, len(links)):
        name = links[i][0][:60]
        url = "https://" + links[i][1]
        fname = f"{str(count).zfill(3)}) {name}"
        
        # Skip images
        if any(x in url.lower() for x in ['.jpg', '.jpeg', '.png', '.webp']):
            await m.reply_text(f"⏭️ Skipping image: {fname[:30]}")
            count += 1
            continue
        
        status = await m.reply_text(f"🔍 {fname[:40]}")
        
        try:
            # Class Plus Resolution
            if 'classplusapp' in url:
                await status.edit(f"🔐 Resolving: {fname[:40]}")
                url = resolve_classplus_url(url, token_manager)
            
            # Download
            ytf = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba" if "youtu" not in url else f"b[height<={quality}][ext=mp4]/bv+ba[ext=m4a]/b"
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{fname}.mp4" -R 25 --fragment-retries 25'
            
            await status.edit(f"📥 Downloading: {fname[:40]}")
            dl = await helper.download_video(url, cmd, fname)
            
            if dl:
                cap = f"**📹 {fname}**\n🎓 {batch}"
                await status.delete()
                await helper.send_vid(bot, m, cap, dl, "no", fname, status)
                count += 1
            else:
                raise Exception("Download failed")
                
        except Exception as e:
            err = str(e)
            await status.edit(f"❌ Failed: {fname[:40]}\n\n`{err[:100]}`")
            if "403" in err:
                await m.reply_text("⚠️ Token expired! Get new token from browser (F12 → Network → x-access-token)")
            time.sleep(2)

async def main():
    if WEBHOOK:
        app = await web_server()
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", PORT).start()

if __name__ == "__main__":
    print("""╔══════════════════════╗\n║ ClassPlus Bot v2.0   ║\n╚══════════════════════╝""")
    
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start())
    print(f"🤖 Bot started | {len(CLASSPLUS_TOKENS)} tokens")
    loop.create_task(main())
    loop.run_forever()
