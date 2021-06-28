import logging
import os
import time
import telegram
import json
from random import randint
from DU.config import *
from DU.dormitoryParser import content_get_list
from DU.telegram_send import telegram_send_message_url, telegram_send_message

def check_admin(chat_id, user_data):
    flag = False
    for comp_user in user_data['admin_user']:
        if chat_id not in comp_user.values():
            continue
        else:
            flag = True
            return flag

    return flag


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