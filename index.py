import re
import threading

import requests
import pandas
from bs4 import BeautifulSoup

off_plan_param = "?completion_status=off-plan"
rent_url = "https://www.propertyfinder.ae/en/search?c=2&fu=0&ob=mr&page=1&rp=y"
buy_url = "https://www.propertyfinder.ae/en/search?c=1&ob=mr&page=1"
def get_soup(_text):
        return BeautifulSoup(_text, features="html.parser")
        
def fetch_property():
    resp = requests.get(rent_url)
    soup = get_soup(resp.text)
    div_tag_list = soup.find_all("div", attrs={"class": "card__content"})
    for item in div_tag_list:
        price = item.find_all("p", attrs={"class": "card-intro__price"})[0]
        type = item.find_all("p", attrs={"class": "card-intro__type"})[0]
        title = item.find_all("h2", attrs={"class": "card-intro__title"})[0]
        location = item.find_all("span", attrs={"class": "card-specifications__location-text"})[0]
        
        beds, baths, area = [x.text for x in item.find_all("p", attrs={"class": "card-specifications__item"})]

