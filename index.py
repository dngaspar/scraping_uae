import threading
import concurrent.futures
import urllib

import requests
import pandas
from bs4 import BeautifulSoup

off_plan_param = "?completion_status=off-plan"
rent_url = "https://www.propertyfinder.ae/en/search?c=2&fu=0&ob=mr&page=1&rp=y"
buy_url = "https://www.propertyfinder.ae/en/search?c=1&ob=mr&page=1"
def get_soup(_text):
        return BeautifulSoup(_text, features="html.parser")
        
def fetch_property(_link):
    url = f"https://www.propertyfinder.ae/en{_link}"
    resp = requests.get(url)
    soup = get_soup(resp.text)
    div_tag_list = soup.find_all("div", attrs={"class": "property-facts__value"})
    _type, _area, _beds, _baths = [x.text for x in div_tag_list]
    location = soup.find_all("div", attrs={"class": "property-location__detail-area"})
    building = location.find_all("div")[0].text
    city = location.find_all("div")[1].text.split(",")[0]
    location = location.find_all("div")[1].text.split(",")[1]
    agent_name = soup.find_all("div", {"class", "property-agent__name"})[0].text
    agent_company = soup.find_all("div", {"class", "property-agent__position-broker-name"})[0].text.split("at")[1]
    return(
        {
            "type": _type,
            "beds": _beds,
            "baths": _baths,
            "area": _area,
            "city": city,
            "location": location,
            "building": building,
            "agent_name": agent_name,
            "agent_company": agent_company,
            "url": url
        }
    )


def main(_url, _category):
    while True:
        urllib.request.urlopen("_url")
        resp = requests.get(_url)
        soup = get_soup(resp.text)
        article_tag_list = soup.find_all("article", attrs={"class": "card"})
        link_list = [x.a["href"] for x in article_tag_list]
        property_obj = {
            "type": [],
            "beds": [],
            "baths": [],
            "area": [],
            "city": [],
            "location": [],
            "building": [],
            "agent_name": [],
            "agent_company": [],
            "url": []
        }

        thread_pool_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for link in link_list:
                thread_pool_list.append(executor.submit(fetch_property, link, _category))
            for item in thread_pool_list:
                for key in property_obj.keys():
                    if item.result():
                        property_obj[key].append(item.result()[key])
                        
        df = pandas.DataFrame(property_obj)
        df.to_csv(f"./propertyfinder/{_category}.csv", mode="a", header=False, index=False)

rent_thread = threading.Thread(target=main, args=(rent_url, "rent"))
sale_thread = threading.Thread(target=main, args=(buy_url, "sale"))
rent_thread.start()
sale_thread.start()
rent_thread.join()
sale_thread.join()