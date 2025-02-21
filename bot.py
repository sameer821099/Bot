import os  
import telebot  
from dotenv import load_dotenv  

# Load environment variables from a .env file  
load_dotenv()  

# Securely access the token  
BOT_TOKEN = os.getenv("BOT_TOKEN")  
bot = telebot.TeleBot(BOT_TOKEN)  

AUTO_REPLY_MESSAGE = "Hey! I'm currently offline. I'll get back to you soon!"  

@bot.message_handler(func=lambda message: True)  
def auto_reply(message):  
    bot.send_message(message.chat.id, AUTO_REPLY_MESSAGE)  

print("Bot is running...")  
bot.polling()