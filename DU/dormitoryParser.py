# -*- coding: utf-8 -*-

import logging
import requests
from bs4 import BeautifulSoup
import json

# 로봇감지 헤더
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

# 파싱 코드
def content_get_list(page):
    # 공지사항 링크 url
    link = "https://dorm.daegu.ac.kr/hakgwa_home/dorm/mobile/sub.php"
    # 공지사항 게시판 url
    url = "https://dorm.daegu.ac.kr/hakgwa_home/dorm/mobile/sub.php?menu=page&menu_id="
    try:
        r = requests.get(url+page)
        r.encoding = 'utf-8'
        bs = BeautifulSoup(r.text, 'html.parser')

        content_list = []

        str_title = bs.select('section.categoryTxt > ul > li')
        title = '[' + str_title[1].get_text() + ']' + '\n'

        # 공지사항 데이터 파싱
        for i in bs.find_all('td', class_='subject'):
            content_title = title + str(i.get_text().strip())
            content_link = link + str(i.find('a').get('href'))
            content_list.append([content_title, content_link])
        
        return content_list
        

    except Exception as e:
        logging.error(e)
        return[]