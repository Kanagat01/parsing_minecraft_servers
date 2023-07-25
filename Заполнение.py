import json
import pandas as pd


data_frame = {'Название сервера': [], 'IP адрес': [], 'Версия': [], 'Сайт сервера': [], 'Группа ВК': [], 'Дискорд': [],
              'Описание': [], 'Основное/Особенности': [], 'Мини-игры': [], 'Плагины': [], 'Моды': [], 'Фотографии': [], 'Баннер': []}

with open('./info.json', encoding='utf-8') as f:
    info = json.load(f)


def some_key(key1, key2):
    try:
        data_frame[key1].append(obj[key2])
    except:
        data_frame[key1].append("")


for obj in info:
    for key in data_frame.keys():
        try:
            data_frame[key].append(obj[key])
        except Exception as ex:
            if key == "Дискорд":
                some_key(key, "Discord")
            elif key == "Группа ВК":
                some_key(key, "Группа сервера в ВК")
            elif key == "Основное/Особенности":
                if "Основное" in obj.keys():
                    some_key(key, "Основное")
                else:
                    some_key(key, "Особенности")
            elif key == "Мини-игры":
                some_key(key, "Мини игры")
            else:
                data_frame[key].append("")

df = pd.DataFrame(data_frame)
df.to_excel('./results.xlsx')
