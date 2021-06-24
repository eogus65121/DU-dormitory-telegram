from os import name
import time
import json
import logging
from typing import Dict

from server import *
from DU.config import *

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
)

def start(update: Update, context: CallbackContext):
    reply_text = "반갑습니다. 대구대학교 기숙사 공지 알리미 입니다. \n 자동공지 시작 을 입력해주세요"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


def check_user(chat_id, user_data):
    flag = True
    for comp_user in user_data['user']:
        if chat_id not in comp_user.values():
            continue
        else:
            flag = False
            return flag

    return flag


def DU_main(update:Update, context: CallbackContext):
    chat_id = update.message.chat.id

    user_data = json.load(open("../data/user.json", "r", encoding="utf-8"))
    print("user_data load success...")

    print("user checking start...")
    if check_user(chat_id, user_data):
        user_data['user'].append({"chat_id":chat_id})
        json.dump(user_data, open("../data/user.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
        print("user_data dump success...")

    reply_text = "자동 공지 서비스가 시작되었습니다. \n 게시판에 새로운 글이 업로드 시 알림이 전송됩니다." 
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

    firstrun = True

    parser(firstrun)


def main():
    config = get_config()

    updater = Updater(token=config['token'])

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)

    message_handler = MessageHandler(Filters.regex('^자동공지 시작$'), DU_main)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)


    updater.start_polling(timeout=3, drop_pending_updates=True)
    updater.idle()


if __name__ == "__main__":
    main()