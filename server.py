# -*- coding: utf-8 -*-

import logging
import os
import time
import telegram
import json
from random import randint
from DU.config import *
from DU.dormitoryParser import content_get_list
from DU.telegram_send import telegram_send_message_url, telegram_send_message

from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)

CHOOSING, ACTION, NOTI_FUNC, ADM_MANAGE, FUN_END, ADD, DELETE = range(7)


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


# 관리자 관리하기 기능
def adm_manage_func(update:Update, context: CallbackContext) -> int:
    Keyboard = [
        [
        InlineKeyboardButton("추가", callback_data='ADD'),
        InlineKeyboardButton("삭제", callback_data='DELETE'),
        ],
        [InlineKeyboardButton("종료", callback_data='FUN_END')]
    ]
    reply_markup = InlineKeyboardMarkup(Keyboard)
    update.message.reply_text("기능을 선택해주세요", reply_markup=reply_markup)
    return ACTION
    

# 관리자 추가    
def add(update:Update, context: CallbackContext) -> int:
    reply_text = "관리자 추가하기 기능입니다. id를 입력하시면 관리자 목록에 추가됩니다. \n (주의) id는 숫자만 입력할 것"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


# 관리자 추가 진행
def add_ing(update:Update, context: CallbackContext) -> int:
    user_text = update.message.text
    admin_data = get_admin()

    if check_admin(user_text ,admin_data):
        context.bot.send_message(chat_id=update.effective_chat.id, text="해당 관리자가 존재합니다, 기능 종료")
    else:
        admin_data['admin_user'].append({"chat_id":int(user_text)})
        json.dump(admin_data, open("../data/admin_user.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
        logging.info("admin_data dump success...")
        context.bot.send_message(chat_id=update.effective_chat.id, text="추가완료, 기능 종료")
    
    return ConversationHandler.END


# 관리자 삭제
def delete(update:Update, context:CallbackContext) -> int:
    reply_text = "관리자 삭제하기 기능입니다. id를 입력하시면 관리자 목록에 추가됩니다. \n (주의) id는 숫자만 입력할 것"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


#관리자 삭제 진행
def delete_ing(update:Update, context: CallbackContext) -> int:
    user_text = int(update.message.text)
    admin_data = get_admin()
    if check_admin(user_text ,admin_data):
        for i in admin_data['admin_user']:
            if user_text == i['chat_id']:
                admin_data['admin_user'].remove(i)
                break
        
        json.dump(admin_data, open("../data/admin_user.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
        logging.info("admin_data dump success...")
        context.bot.send_message(chat_id=update.effective_chat.id, text="제거완료, 기능 종료")
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="해당 관리자가 존재하지 않습니다, 기능 종료")
    
    return ConversationHandler.END


# 관리자 기능 선택
def func_choice(update:Update, context:CallbackContext) ->None :
    Keyboard = [
        [
        InlineKeyboardButton("전체공지", callback_data='NOTI_FUNC'),
        InlineKeyboardButton("관리자 관리", callback_data='ADM_MANAGE'),
        ],
        [InlineKeyboardButton("종료", callback_data='FUN_END')]
    ]
    reply_markup = InlineKeyboardMarkup(Keyboard)
    update.message.reply_text("기능을 선택해주세요", reply_markup=reply_markup)
    return ACTION


# 관리자 명단에서 관리자 확인
def check_admin(chat_id, user_data):
    flag = False
    for comp_user in user_data['admin_user']:
        if chat_id not in comp_user.values():
            continue
        else:
            flag = True
            return flag

    return flag

#텔레그램 전송
def server_send_telegram(data):
    try:
        config = get_config()
        content = data[0]
        url = data[1]
        user_data = get_user()
        for i in user_data['user']:
            chat_id = i['chat_id']
            telegram_send_message_url(chat_id, config, content, url)
        logging.info("data send success")
    except Exception as e:
        logging.info(e)
    pass


# 모든 인원에게 데이터 전송
def server_notice_echo(data):
    try:
        config = get_config()
        user_data = get_user()
        for i in user_data['user']:
            chat_id = i['chat_id']
            telegram_send_message(chat_id, config, data)
        logging.info("data send success")
    except Exception as e:
        logging.info(e)
    pass


# 기숙사 게시판 파싱 및 전송 코드
def parser(firstrun):
    page = [32, 33, 29]
    config = get_config()
    current_data = []
    
    if os.path.exists("../data/dormitory.json"):
        stored_data = get_dormitory()
        logging.info("json load success...")
        if firstrun == True:
            return

    logging.info("parser start...")

    for page_num in page:
        current_data = current_data + content_get_list(str(page_num))
        time.sleep(randint(1, 3))

    logging.info("parser end...")

    logging.info("compare start...")

    for c_data in current_data:
        if c_data not in stored_data:
            server_send_telegram(c_data)
            logging.info("send_telegram success waiting 3sec...")
            time.sleep(3)

    logging.info("compare end waiting 10sec...")
    time.sleep(10)
    
    logging.info("dormitory.json dump start...")
    json.dump(current_data, open("../data/dormitory.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    logging.info("dump end...")


def main():
    firstrun = False
    parser(firstrun)
    time.sleep(10)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(randint(500, 600))