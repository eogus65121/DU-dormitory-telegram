import json

def get_general():
    return json.load(open("../data/general.json", "r", encoding="utf-8"))

def get_resident():
    return json.load(open("../data/resident.json", "r", encoding="utf-8"))

def get_resignation():
    return json.load(open("../data/resignation.json", "r", encoding="utf-8"))

# biho_RC 페이지는 권한문제로 잠시 보류
def get_biho_RC():
    return json.load(open("../data/biho_RC.json", "r", encoding="utf-8"))
