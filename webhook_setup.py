import os
import telebot

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

bot.remove_webhook()
bot.set_webhook(os.environ.get('WEBHOOK_URL'))

