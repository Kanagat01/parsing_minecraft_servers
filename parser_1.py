# import asyncio
# import json
# import aiohttp
# from bs4 import BeautifulSoup as BS


# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()


# async def parse_server_info(url):
#     async with aiohttp.ClientSession() as session:
#         try:
#             html = await fetch(session, url)
#             soup = BS(html, "html.parser")

#             info = {}
#             keys = ["IP адрес", "Версия", "Сайт сервера",
#                     "Группа сервера в ВК", "Discord", "Основное", "Мини игры", "Плагины", "Моды"]

#             info["Название сервера"] = soup.select_one(
#                 "#about > div > h1").text.replace(" сервер Майнкрафт", "")
#             info["Описание"] = "\n".join(
#                 [el.text for el in soup.select("#description > p")])

#             banner = soup.select_one("div.banner.text-center > img")
#             try:
#                 async with session.get(banner.get("data-src")) as response:
#                     r = await response.read()
#                     title = info["Название сервера"].replace(
#                         " ", "_")
#                     with open(f"banners/{title}.gif", "wb") as f:
#                         f.write(r)
#                     info["Баннер"] = f"./banners/{title}.gif"
#             except Exception as ex:
#                 print(ex)
#                 info["Баннер"] = ""

#             images = soup.select("#screenshots > a > img") + \
#                 soup.select("#screenshots_all > a > img")
#             images = [img.get("data-src") for img in images]
#             try:
#                 lst = []
#                 for idx, src in enumerate(images):
#                     async with session.get(src) as response:
#                         r = await response.read()
#                         title = info["Название сервера"].replace(
#                             " ", "_")
#                         with open(f"screenshots/{title}_{idx}.jpg", "wb") as f:
#                             f.write(r)
#                         lst.append(f"screenshots/{title}_{idx}.jpg")
#                 info["Фотографии"] = ", ".join(lst)
#             except Exception as ex:
#                 print(ex)
#                 info["Фотографии"] = ""

#             elems = soup.select(
#                 "body > div.wrapper-main > div.container.page-server > div.content-server > table > tr")
#             for el in elems:
#                 key = el.select_one("td:nth-child(1)").text.replace(":", "")
#                 if key in keys:
#                     vals = el.select("td:nth-child(2) > a")
#                     if vals is not None and len(vals) >= 2:
#                         info[key] = ", ".join([val.text for val in vals])
#                     else:
#                         info[key] = el.select_one("td:nth-child(2)").text

#             for key in keys:
#                 if key not in info.keys():
#                     info[key] = ""

#             print(info["Название сервера"])
#             return info
#         except Exception as ex:
#             print(ex)
#             return None


# async def main():
#     print("Starting...")
#     links_lst = open("./links.txt").read().split("\n")
#     i = 0
#     while i * 500 <= len(links_lst):
#         tasks = []
#         for link in links_lst[i*500:(i+1)*500]:
#             task = asyncio.create_task(parse_server_info(link))
#             tasks.append(task)
#         print("Tasks created. Getting results...")

#         for res in asyncio.as_completed(tasks):
#             info = await res
#             if info is not None:
#                 json_info = json.dumps(info, ensure_ascii=False)
#                 with open("./info.json", "a", encoding="utf-8") as f:
#                     f.write(f"{json_info},\n")
#             await asyncio.sleep(0)  # Добавлено ожидание
#         print(f"Iteration {i}")
#         i += 1

# if __name__ == "__main__":
#     asyncio.run(main())

import json


with open('./info.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

titles = []
for obj in data:
    titles.append(obj["Название сервера"])

titles2 = open("./links2.txt", encoding="utf-8").read().split("\n")
titles2 = [x.split("_:_")[0] for x in titles2]
titles.extend(titles2)
titles = set(titles)
with open("./titles.txt", "a", encoding="utf-8") as f:
    for title in titles:
        f.write(f"{title}\n")

# links = set(open("./links2.txt", encoding="utf-8").read().split("\n"))
# with open("./new_links.txt", "a", encoding="utf-8") as f:
#     for title in links:
#         f.write(f"{title}\n")
