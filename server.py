import logging
import os
import time
import telegram
import json
from random import randint
from DU.config import *
from DU.dormitoryParser import content_get_list
from DU.telegram_send import send_message

def send_telegram(data):
    try:
        config = get_config()
        content = data[0]
        url = data[1]
        send_message(config, content, url)
        logging.info("data send success")
    except Exception as e:
        logging.error(e)
    pass


def parser():
    page = [32, 33, 29]
    config = get_config()
    current_data = []
    
    if os.path.exists("../data/dormitory.json"):
        stored_data = json.load(open("../data/dormitory.json", "r", encoding="utf-8"))

    logging.info("parser start...")

    for page_num in page:
        current_data = current_data + content_get_list(str(page_num))
        time.sleep(randint(1, 3))

    logging.info("parser end...")

    logging.info("compare start...")

    for c_data in current_data:
        if c_data not in stored_data:
            send_telegram(c_data)
            logging.info("send_telegram success waiting 3sec...")
            time.sleep(3)

    logging.info("compare end waiting 10sec...")
    time.sleep(10)
    
    logging.info("dormitory.json dump start...")
    json.dump(current_data, open("../data/dormitory.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    logging.info("dump end...")

parser()