import asyncio
import json
import aiohttp
from aiohttp.client_exceptions import *
from bs4 import BeautifulSoup as BS

keys = ["IP адрес", "Версия", "Сайт сервера", "Группа ВК",
        "Дискорд", "Особенности", "Мини-игры", "Плагины", "Моды"]
results = []


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape_data(title, link, banner):
    async with aiohttp.ClientSession() as session:
        try:
            info = {}
            info["Название сервера"] = title
            info["Баннер"] = banner
            html = await fetch(session, f"https://hotmc.ru{link}")
            soup = BS(html, "html.parser")
            desc = soup.select_one(
                "#server > div.section.server-description > p")
            desc = desc.text if desc is not None else ""
            info["Описание"] = desc.strip()
            try:
                images = soup.select(
                    ".section > #slider-screenshots > a.fancybox.img-block")
                photos = []
                for idx, href in enumerate([x.get("href") for x in images]):
                    try:
                        async with session.get(href) as response:
                            data = await response.read()
                            ext = "png" if "png" in href else "jpg"
                            filename = f"./screenshots/{title}_{idx}.{ext}"
                            with open(filename, "wb") as f:
                                f.write(data)
                            photos.append(filename)
                    except Exception as ex:
                        print(ex)
                info["Фотографии"] = ", ".join(photos)
            except:
                info["Фотографии"] = ""
            rows = soup.select("#server > form > div.form-group")
            for row in rows:
                key = row.select_one("label").text.strip().replace(":", "")
                if key in keys:
                    div = row.select_one("div")
                    if div.select_one("input") is not None:
                        info[key] = div.select_one("input").get("value")
                    elif div.select("div > a") is not None:
                        info[key] = ", ".join(
                            [x.text for x in div.select("div > a")])
                    elif div.select_one("a") is not None:
                        info[key] = div.select_one("a").text
            results.append(info)
            print(info["Название сервера"])
        except (ClientConnectorError, ServerDisconnectedError, ClientOSError, ClientResponseError, Exception) as ex:
            print(ex)
            with open("./exceptions.txt", "a", encoding="utf-8") as f:
                f.write(f"{title}_:_{link}_:_{banner}\n")


async def main():
    data = open("./links2.txt", encoding="utf-8").read().split("\n")

    i = 0
    while i * 100 <= len(data):
        tasks = []
        for x in data[i*100:(i+1)*100]:
            try:
                title, link, banner = x.split("_:_")
                tasks.append(scrape_data(title, link, banner))
            except Exception as ex:
                print(ex)
                with open("./exceptions.txt", "a", encoding="utf-8") as f:
                    f.write(f"{x}\n")
        await asyncio.gather(*tasks)
        with open("./info.json", "a", encoding="utf-8") as f:
            global results
            json.dump(results, f, indent=4, ensure_ascii=False)
            results = []
        i += 1


if __name__ == "__main__":
    asyncio.run(main())

