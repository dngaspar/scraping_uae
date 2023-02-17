import re
import threading

import requests
import pandas
from bs4 import BeautifulSoup
from soupsieve import purge

header = {"Content-Type": "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
off_plan_param = "?completion_status=off-plan"
ready_plan_param = "?completion_status=ready"

def get_soup(_text):
    return BeautifulSoup(_text, features="html.parser")

def main(category, off_plan_flag):
    idx = 1
    path = f"./bayut/{category}"
    if off_plan_flag:
        path += "-off"
    path += ".csv"
    while True:
        if idx == 1:
            url = f"https://www.bayut.com/{category}/property/uae/"
        else:
            url = f"https://www.bayut.com/{category}/property/uae/page-{idx}/"
        if category == "to-rent":
            url += "?rent_frequency=any"
        else:
            if off_plan_flag:
                url += off_plan_param
            else:
                url += ready_plan_param
        resp = requests.get(url, headers=header)
        soup = get_soup(resp.text)
        li_tag_list = soup.find_all("li", attrs={"role": "article"})
        link_obj = {
            "link": []
        }
        if category == "to-rent":
            link_obj["frequency"] = []
        if not li_tag_list:
            break
        link_list = []
        for item in li_tag_list:
            link = item.find_all("a", attrs={"aria-label": "Listing link"})[0]["href"]
            link_list.append(link)


        df = pandas.DataFrame(link_obj)
        df.to_csv(path, mode="a", header=False, index=False)
        idx += 1

category_list = ["to-rent", "for-sale"]
threading_list = []
for category in category_list:
    if category == "for-sale":
        item_off = threading.Thread(target=main, args=(category, True))
        threading_list.append(item_off)
        item_off.start()

    item = threading.Thread(target=main, args=(category, False))
    threading_list.append(item)
    item.start()

for item in threading_list:
    item.join()