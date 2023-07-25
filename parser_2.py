import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup as BS


titles = open("./titles.txt", encoding="utf-8").read().split("\n")
keys = ["IP адрес", "Версия", "Сайт сервера",
        "Мини-игры", "Плагины", "Моды"]
results = []


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_links(page_num):
    url = f"https://monitoringminecraft.ru/{page_num}/"
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, url)
        soup = BS(html, "html.parser")

        elems = soup.select("#servers > table > tbody > tr")
        for el in elems:
            try:
                info = {}
                link = el.select_one("td.two > div > a")
                if link.text not in titles:
                    info["Название сервера"] = link.text
                    banner = el.select_one("td:nth-child(3) > a > img")
                    if banner is not None:
                        async with session.get(banner.get("data-src")) as response:
                            r = await response.read()
                            title = info["Название сервера"].replace(
                                " ", "_")
                            with open(f"./banners/{title}.gif", "wb") as f:
                                f.write(r)
                            info["Баннер"] = f"./banners/{title}.gif"
                    else:
                        info["Баннер"] = ""

                    url = "https://monitoringminecraft.ru" + link.get("href")
                    async with aiohttp.ClientSession() as session2:
                        html = await fetch_url(session2, url)
                        soup = BS(html, "html.parser")
                        info["Описание"] = soup.select_one(
                            "td.desc").text
                        images = soup.select(
                            "#server_page > div.box.visible > div.sidebar.sright > div.images > a")
                        if images is not None:
                            photos = []
                            for idx, href in enumerate(["https://monitoringminecraft.ru" + x.get("href") for x in images]):
                                title = info["Название сервера"]
                                try:
                                    async with session.get(href) as response:
                                        r = await response.read()
                                        with open(f"./screenshots/{title}_{idx}.jpg", "wb") as f:
                                            f.write(r)
                                        photos.append(
                                            f"./screenshots/{title}_{idx}.jpg")
                                except Exception as ex:
                                    print(ex)
                            info["Фотографии"] = ", ".join(photos)
                        data = soup.select(
                            "#server_page > div.box.visible > div.sleft > table > tr")
                        for tr in data:
                            key = tr.select_one(
                                "td:nth-child(1)").text.replace(":", "").strip()
                            if key in keys:
                                val = tr.select_one("td:nth-child(2)")
                                if val.select("a") is not None:
                                    info[key] = ", ".join(
                                        [x.text for x in val.select("a")])
                                else:
                                    info[key] = val.text
                print(info["Название сервера"])
                results.append(info)
            except aiohttp.ClientConnectorError as ex:
                print(ex)
                return []

            except aiohttp.ClientError as ex:
                print(ex)
                return []

            except Exception as ex:
                print(ex)
                return []


async def main():
    tasks = [asyncio.create_task(get_links(""))]
    for page_num in range(2, 44):
        task = asyncio.create_task(get_links(page_num))
        tasks.append(task)

    for res in asyncio.as_completed(tasks):
        await res

    print(len(results))
    with open("./info.json", "a", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())
