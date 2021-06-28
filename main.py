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

reply_start = [['챗봇시작']]
task_function = [
    ['전체공지'],
    ['추가기능 뭐하지']
]
reply_func = [['기능선택']]

markup_start = ReplyKeyboardMarkup(reply_start, one_time_keyboard=True)
markup_function_choice = ReplyKeyboardMarkup(task_function, one_time_keyboard=True)
markup_func = ReplyKeyboardMarkup(reply_func, one_time_keyboard=True)

CHOOSING, TYPING_FUNC = range(2)

# telegram bot 첫 시작 /start command handler
def start(update: Update, context: CallbackContext):
    reply_text = "반갑습니다. 대구대학교 기숙사 공지 알리미 입니다. \n '챗봇시작' 버튼 선택 혹은 '챗봇시작'을 입력해주세요"
    update.message.reply_text(reply_text, reply_markup=markup_start)


# 기존 chat_id가 데이터에 저장되어 있는지 확인
def check_user(chat_id, user_data):
    flag = True
    for comp_user in user_data['user']:
        if chat_id not in comp_user.values():
            continue
        else:
            flag = False
            return flag

    return flag


def check_admin(chat_id, user_data):
    flag = False
    for comp_user in user_data['admin_user']:
        if chat_id not in comp_user.values():
            continue
        else:
            flag = True
            return flag

    return flag


def echo_notice(update:Update, context: CallbackContext) -> int:
    user_text = update.message.text
    print(user_text)
    server_notice_echo(user_text)
    return ConversationHandler.END


def notice_task(update:Update, context: CallbackContext) -> int:
    reply_text = "전체공지 기능입니다. 내용 입력 시 모든 사용자에게 전송 후 관리자 기능이 자동 종료됩니다."
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


def choice_func(update:Update, context: CallbackContext) -> int:
    reply_text = "원하는 기능을 선택해주세요"
    update.message.reply_text(reply_text, reply_markup=markup_function_choice)
    return TYPING_FUNC


def task(update:Update, context: CallbackContext) -> int:
    reply_text1 = "관리자 기능입니다."
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text1)
    user_data = get_admin()
    print("user checking admin...")

    if check_admin(chat_id, user_data):
        print("admin이 맞음 해당 기능 실행")
        update.message.reply_text("관리자 인증 성공", reply_markup=markup_func)
        return CHOOSING
    else:
        reply_text2 = "관리자가 아닙니다. 해당 기능을 종료합니다."
        context.bot.send_message(chat_id=update.effective_chat.id, text = reply_text2)
        return ConversationHandler.END


def done(update: Update, context: CallbackContext) -> int:
    reply_text = "관리자 기능 종료"
    context.bot.send_message(chat_id=update.effective_chat.id, text = reply_text)
    return ConversationHandler.END


# 자동공지 서비스 시작 command handler
def DU_main(update:Update, context: CallbackContext):
    chat_id = update.message.chat.id

    user_data = get_user()
    print("user_data load success...")

    print("user checking start...")
    if check_user(chat_id, user_data):
        user_data['user'].append({"chat_id":chat_id})
        json.dump(user_data, open("../data/user.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
        print("user_data dump success...")
    else:
        print("user exist")

    reply_text = "자동 공지 서비스가 시작되었습니다. \n 게시판에 새로운 글이 업로드 시 알림이 전송됩니다." 
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

    firstrun = True

    parser(firstrun)


def main():
    config = get_config()
    updater = Updater(token=config['token'])
    dispatcher = updater.dispatcher

    #start_handler = CommandHandler('start', start)

    #message_handler = MessageHandler(Filters.regex('^챗봇시작$'), DU_main)
    #dispatcher.add_handler(start_handler)

    task_handler = ConversationHandler(
        entry_points=[CommandHandler('task', task)],
        states={
            CHOOSING:[
                MessageHandler(Filters.regex('^기능선택$'), choice_func)
            ],
            TYPING_FUNC:[
                MessageHandler(Filters.regex('^전체공지$'), notice_task),
                MessageHandler(Filters.text & ~Filters.command, echo_notice)
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^챗봇시작$'), DU_main))
    dispatcher.add_handler(task_handler)

    updater.start_polling(timeout=3, drop_pending_updates=True)
    updater.idle()


if __name__ == "__main__":
    main()