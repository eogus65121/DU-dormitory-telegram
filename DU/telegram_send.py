import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_message(config, content, url):
    bot = telegram.Bot(token=config['token'])
    reply_markup =[[InlineKeyboardButton(text="바로가기", url=url)]]
    bot.sendMessage(chat_id=config['chat_id'], text=content, reply_markup=InlineKeyboardMarkup(reply_markup))