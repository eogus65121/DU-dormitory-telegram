from os import name
import time
import json
import logging
from typing import Dict
from telegram.callbackquery import CallbackQuery

from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

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
    CallbackQueryHandler,
    CallbackContext,
)

reply_start = [['챗봇시작']]
task_func_noti = [['전체공지']]
task_func_add_adm = [['관리자 추가']]
task_func_end = [['Done']]
reply_func = [['기능선택']]
reply_YS = [['Yes'], ['No']]


markup_start = ReplyKeyboardMarkup(reply_start, one_time_keyboard=True)
markup_func_noti = ReplyKeyboardMarkup(task_func_noti, one_time_keyboard=True)
markup_func_add_adm = ReplyKeyboardMarkup(task_func_add_adm, one_time_keyboard=True)
markup_func_end = ReplyKeyboardMarkup(task_func_end, one_time_keyboard=True)
markup_func = ReplyKeyboardMarkup(reply_func, one_time_keyboard=True)
markup_YS = ReplyKeyboardMarkup(reply_YS, one_time_keyboard=True)

#CHOOSING, NOTI_FUNC, ADD_ADMIN = range(3)
CHOOSING, ACTION, NOTI_FUNC, ADD_ADM, FUN_END = range(5)

# telegram bot 첫 시작 /start command handler
def start(update: Update, context: CallbackContext):
    reply_text = "반갑습니다. 대구대학교 기숙사 공지 알리미 입니다. \n '챗봇시작' 버튼 선택 혹은 '챗봇시작'을 입력해주세요"
    update.message.reply_text(reply_text, reply_markup=markup_start)
    return ConversationHandler.END


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

# 공지 echo 메시지 전송
def echo_notice(update:Update, context: CallbackContext) -> int:
    user_text = update.message.text
    server_notice_echo(user_text)
    reply_text="전송완료, 기능 종료"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    return ConversationHandler.END

# 공지 기능 시작
def notice_task(update:Update, context: CallbackContext) -> int:
    reply_text = "전체공지 기능입니다. 내용 입력 시 모든 사용자에게 전송됩니다."
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

def add_admin_func(update:Update, context: CallbackContext) -> int:
    reply_text = "관리자 계정 추가하기 기능입니다. id를 입력시 관리자로 등록됩니다."
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    return ConversationHandler.END

# def add_id_check(update:Update, context: CallbackContext) -> int:
#     user_id = update.message.text
#     reply_text = "추가를 워하는 id가 " + str(user_id) + "맞습니까? \n YES = 추가하기 // NO = 처음으로(/task 명령부터 재실행)"
#     update.message.reply_text(reply_text, reply_markup=markup_YS)


# def add_admin(update:Update, context:CallbackContext, data) -> int:
#     admin_data = get_admin()
#     admin_data['admin_user'].append({"chat_id":data})
#     json.dump(admin_data, open("../data/user.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)


# 관리자 기능 실행
def task(update:Update, context: CallbackContext) -> int:
    reply_text1 = "관리자 기능입니다."
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text1)
    user_data = get_admin()
    logging.info("user checking admin...")

    if check_admin(chat_id, user_data):
        update.message.reply_text("관리자 인증 성공", reply_markup=markup_func)
        return CHOOSING
    else:
        reply_text2 = "관리자가 아닙니다. 해당 기능을 종료합니다."
        context.bot.send_message(chat_id=update.effective_chat.id, text = reply_text2)
        return ConversationHandler.END


def action(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id

    if query.data == "NOTI_FUNC":
        reply_text = "하단 전체공지 버튼을 눌러주세요"
        context.bot.send_message(chat_id=chat_id, text =reply_text, reply_markup=markup_func_noti)
        return NOTI_FUNC
    elif query.data == "ADD_ADM":
        reply_text = "하단 관리자 추가 버튼을 눌러주세요"
        context.bot.send_message(chat_id=chat_id, text =reply_text, reply_markup=markup_func_add_adm)
        return ADD_ADM
    elif query.data == "FUN_END":
        reply_text = "하단 종료 버튼을 눌러주세요"
        context.bot.send_message(chat_id=chat_id, text =reply_text, reply_markup=markup_func_end)
        return FUN_END


def func_choice(update:Update, context:CallbackContext) ->None :
    Keyboard = [
        [
        InlineKeyboardButton("전체공지", callback_data='NOTI_FUNC'),
        InlineKeyboardButton("관리자추가", callback_data='ADD_ADM'),
        ],
        [InlineKeyboardButton("종료", callback_data='FUN_END')]
    ]
    reply_markup = InlineKeyboardMarkup(Keyboard)
    update.message.reply_text("기능을 선택해주세요", reply_markup=reply_markup)
    return ACTION

# conversation handler 종료
def done(update: Update, context: CallbackContext) -> int:
    reply_text = "관리자 기능이 종료되었습니다."
    context.bot.send_message(chat_id=update.effective_chat.id, text = reply_text)
    return ConversationHandler.END


def id_check(update: Update, context: CallbackContext) -> int:
    my_chat_id = update.message.chat.id
    reply_text = "나의 chat_id = " + str(my_chat_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


# 자동공지 서비스 시작 first run command handler
def DU_main(update:Update, context: CallbackContext):
    chat_id = update.message.chat.id

    user_data = get_user()
    logging.info("user_data load success...")

    logging.info("user checking start...")
    if check_user(chat_id, user_data):
        user_data['user'].append({"chat_id":chat_id})
        json.dump(user_data, open("../data/user.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
        logging.info("user_data dump success...")
    else:
        logging.info("user exist...")

    reply_text = "자동 공지 서비스가 시작되었습니다. \n 게시판에 새로운 글이 업로드 시 알림이 전송됩니다." 
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

    firstrun = True

    parser(firstrun)


def main():
    config = get_config()
    updater = Updater(token=config['token'])
    dispatcher = updater.dispatcher

    task_handler = ConversationHandler(
        entry_points=[CommandHandler('task', task)],
        states={
            CHOOSING:[
                MessageHandler(Filters.regex('^기능선택$'), func_choice),
            ],
            ACTION:[
                CallbackQueryHandler(action)
            ],
            NOTI_FUNC:[
                MessageHandler(Filters.regex('^전체공지$'), notice_task),
                MessageHandler(Filters.text & ~Filters.command, echo_notice)
            ],
            ADD_ADM:[
                MessageHandler(Filters.regex('^관리자 추가$'), add_admin_func)
            ],
            FUN_END:[
                MessageHandler(Filters.regex('^종료$'), done)
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^done$'), done)]
    )

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('id', id_check))
    dispatcher.add_handler(MessageHandler(Filters.regex('^챗봇시작$'), DU_main))
    dispatcher.add_handler(task_handler)

    updater.start_polling(timeout=3, drop_pending_updates=True)
    updater.idle()


if __name__ == "__main__":
    main()