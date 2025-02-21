import telebot
import yt_dlp
import instaloader
import os
import requests

# 🎯 Replace this with your Telegram Bot Token
BOT_TOKEN = "7548871019:AAHwFWLMgq8D2rwtYf6Y5CGYtwlILQiS1G0"
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize Instagram downloader
insta_loader = instaloader.Instaloader()

# ✨ Function to download YouTube video
def download_youtube(url, audio_only=False):
    ydl_opts = {
        'format': 'bestaudio' if audio_only else 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt'  # ← This line enables authentication
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
# 📸 Function to download Instagram videos
def download_instagram(url):
    os.system(f"instaloader -- -{url.split('/')[-2]}")  # Downloads to current dir
    return f"{url.split('/')[-2]}.mp4"

# 📂 Function to download Tarabox files
def download_tarabox(url):
    response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as file:
        file.write(response.content)
    return filename

# 👋 Welcome Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 **Hello!** I am your **Downloader Bot**! 🚀\n\n"
                          "📥 **Send me a link** from:\n"
                          "🔹 **YouTube** (MP4/MP3)\n"
                          "🔹 **Instagram** (Videos)\n"
                          "🔹 **Tarabox** (Files)\n\n"
                          "⚡ Just drop a link, and I'll take care of the rest! 😉")

# 🎯 Handle User Messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text

    if "youtube.com" in url or "youtu.be" in url:
        bot.send_message(message.chat.id, "🎬 **Downloading YouTube video... Please wait!** ⏳")
        filename = download_youtube(url)
        bot.send_message(message.chat.id, "✅ **Download Complete! Sending your video...** 🎥")
        with open(filename, "rb") as video:
            bot.send_video(message.chat.id, video)
        os.remove(filename)

    elif "instagram.com" in url:
        bot.send_message(message.chat.id, "📸 **Downloading Instagram video... Hang tight!** 🔄")
        filename = download_instagram(url)
        bot.send_message(message.chat.id, "✅ **Instagram video downloaded! Sending now...** 📩")
        with open(filename, "rb") as video:
            bot.send_video(message.chat.id, video)
        os.remove(filename)

    elif "tarabox.com" in url:
        bot.send_message(message.chat.id, "📂 **Fetching file from Tarabox...** ⏳")
        filename = download_tarabox(url)
        bot.send_message(message.chat.id, "✅ **File ready! Sending now...** 📤")
        with open(filename, "rb") as file:
            bot.send_document(message.chat.id, file)
        os.remove(filename)

    else:
        bot.send_message(message.chat.id, "❌ **Invalid URL!**\n"
                                          "🚀 Please send a valid **YouTube, Instagram, or Tarabox** link.")

print("🤖 Bot is running...")
bot.polling()
