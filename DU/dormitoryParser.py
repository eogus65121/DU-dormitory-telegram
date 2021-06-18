import logging
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

def content_get_list(url, page):
    link = "https://dorm.daegu.ac.kr/hakgwa_home/dorm/mobile/sub.php"
    try:
        r = requests.get(url+page)
        r.encoding = 'utf-8'
        bs = BeautifulSoup(r.text, 'html.parser')

        content_list = []

        for i in bs.find_all('td', class_='subject'):
            content_title = str(i.get_text().strip())
            content_link = link + str(i.find('a').get('href'))
            content_list.append([content_title, content_link])
        
        return content_list
        

    except Exception as e:
        logging.error(e)
        return[]


# content_get_list(url, page)
# url = "https://dorm.daegu.ac.kr/hakgwa_home/dorm/mobile/sub.php?menu=page&menu_id="
# page = "32, 33, 29, 1042"