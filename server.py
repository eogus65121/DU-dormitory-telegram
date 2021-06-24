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
        user_data = get_user()
        for i in user_data['user']:
            chat_id = i['chat_id']
        send_message(chat_id, config, content, url)
        print("data send success")
    except Exception as e:
        print(e)
    pass


def parser(firstrun):
    page = [32, 33, 29]
    config = get_config()
    current_data = []
    
    if os.path.exists("../data/dormitory.json"):
        stored_data = json.load(open("../data/dormitory.json", "r", encoding="utf-8"))
        print("json load success...")

    print("parser start...")

    for page_num in page:
        current_data = current_data + content_get_list(str(page_num))
        time.sleep(randint(1, 3))

    print("parser end...")

    print("compare start...")

    for c_data in current_data:
        if c_data not in stored_data:
            send_telegram(c_data)
            print("send_telegram success waiting 3sec...")
            time.sleep(3)

    print("compare end waiting 10sec...")
    time.sleep(10)
    
    print("dormitory.json dump start...")
    json.dump(current_data, open("../data/dormitory.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
    print("dump end...")


def main():
    firstrun = False
    parser(firstrun)
    time.sleep(10)

if __name__ == "__main__":
    #while True:
    #    main()
    #    time.sleep(randint(500, 600))
    main()