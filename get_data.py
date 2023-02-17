import requests
from bs4 import BeautifulSoup as BS
import time
from datetime import datetime, timedelta
from tqdm import tqdm

urls_data = []
result_data = []
main_url = "https://www.list.am"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def get_main_urls():
    global urls_data
    print("Starting....")
    url = "https://www.list.am/category/60?cmtype=1&type=1&po=1&n=1&crc=-1&gl=2"

    r = requests.get(url, headers=headers)
    soup = BS(r.content, "html.parser")
    main_div = soup.find_all("div", class_="dl")
    for div in main_div:
        for link in div.find_all('a'):
            href = link.get('href')
            if href and "/item/" in href:
                urls_dict = {"url": href}
                urls_data.append(urls_dict)


def check_day(date_str):
    dates = datetime.strptime(date_str, '%d.%m.%Y').date()
    today = datetime.today().date()
    yesterday = (datetime.today() - timedelta(days=1)).date()
    if dates == today or dates == yesterday:
        return True
    else:
        return False


def get_current_data():
    global urls_data, result_data
    result_data.clear()
    print(len(urls_data))
    for items_url in urls_data:
        order_url = main_url + items_url["url"]
        new_r = requests.get(order_url, headers=headers)
        new_soup = BS(new_r.content, "html.parser")
        footer_div = new_soup.find_all("div", class_="footer")
        footer_soup = BS(str(footer_div), "html.parser")
        spans = footer_soup.find_all('span')
        second_span = spans[1]
        date = second_span.text.split(" ")[2]
        res = check_day(date)
        if res:
            divs = new_soup.find_all("div", class_='vih')
            for name in divs:
                try:
                    item = name.find("h1").text.strip()
                    price = name.find("span").text.strip()
                    result_dict = {
                        "name": item,
                        "price": price,
                        "url": order_url
                    }
                    result_data.append(result_dict)
                    print("Found")
                except Exception:
                    pass
        else:
            print("Nothing new")
        time.sleep(1)
    return result_data


def run():
    get_main_urls()
    time.sleep(1)
    results = get_current_data()
    return results


if __name__ == "__main__":
    run()
