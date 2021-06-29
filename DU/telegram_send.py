# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def telegram_send_message_url(chat_id, config, content, url):
    bot = telegram.Bot(token=config['token'])
    reply_markup =[[InlineKeyboardButton(text="바로가기", url=url)]]
    bot.sendMessage(chat_id=chat_id, text=content, reply_markup=InlineKeyboardMarkup(reply_markup))

def telegram_send_message(chat_id, config, text):
    bot = telegram.Bot(token=config['token'])
    bot.sendMessage(chat_id=chat_id, text = text)