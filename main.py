import os
import asyncio
import yt_dlp
from pyrogram import Client, filters

# Get your bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Initialize the bot
app = Client(
    "video_downloader_bot",
    api_id=123456,  # Use dummy API ID, not needed for bot-only usage
    api_hash="0123456789abcdef0123456789abcdef",  # Use dummy API HASH
    bot_token=BOT_TOKEN
)

# Download options for yt-dlp
ydl_opts = {
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads/ folder
    'format': 'best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
}

# Make sure downloads folder exists
os.makedirs("downloads", exist_ok=True)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Send me a video link from YouTube, TikTok, Instagram, etc., and I will download it for you!")

@app.on_message(filters.text & ~filters.command(["start"]))
async def download_video(client, message):
    url = message.text.strip()

    if not (url.startswith("http://") or url.startswith("https://")):
        await message.reply("Please send a valid URL!")
        return

    msg = await message.reply("Downloading your video... please wait.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        await message.reply_video(video_path, caption="Here is your video!")
        os.remove(video_path)

    except Exception as e:
        await msg.edit(f"Failed to download: {e}")

if __name__ == "__main__":
    app.run()
