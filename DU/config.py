import json

def get_config():
    return json.load(open("../data/config.json", "r", encoding="utf-8"))

#일반공지
def get_general():
    return json.load(open("../data/general.json", "r", encoding="utf-8"))

#자치회
def get_resident():
    return json.load(open("../data/resident.json", "r", encoding="utf-8"))

#입퇴사
def get_resignation():
    return json.load(open("../data/resignation.json", "r", encoding="utf-8"))

# biho_RC 페이지는 권한문제로 잠시 보류
def get_biho_RC():
    return json.load(open("../data/biho_RC.json", "r", encoding="utf-8"))

#공지 데이터 통합
def get_dormitory():
    return json.load(open("../data/dormitory.json", "r", encoding="utf-8"))

# user data
def get_user():
    return json.load(open("../data/user.json", "r", encoding="utf-8"))