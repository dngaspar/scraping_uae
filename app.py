from operator import attrgetter
import requests
import pandas
from bs4 import BeautifulSoup

def get_soup(_text):
        return BeautifulSoup(_text, features="html.parser")

idx = 1
while True:
    if idx == 1:
        url = "https://www.bayut.com/for-sale/property/uae/"
    else:
        url = f"https://www.bayut.com/for-sale/property/uae/page-{idx}/"
    resp = requests.get(url)
    soup = get_soup(resp.text)
    li_tag_list = soup.find_all("li", attrs={"role": "article"})
    property_obj = {
        "price": [],
        "location": [],
        "beds": [],
        "baths": [],
        "sqft": [],
        "title": [],
        "type": []
    }
    if not li_tag_list:
        break
    for item in li_tag_list:
        price = item.find_all("span", attrs={"aria-label": "Price"})[0].text
        property_obj["price"].append(price)
        
        location = item.find_all("div", attrs={"aria-label": "Location"})[0].text
        property_obj["location"].append(location)

        title = item.find_all("h2", attrs={"aria-label": "Title"})[0].text
        property_obj["title"].append(title)
        
        type = item.find_all("div", attrs={"aria-label": "Type"})[0].text
        property_obj["type"].append(title)

        beds_element = item.find_all("span", attrs={"aria-label": "Beds"})
        if beds_element:
            beds = beds_element[0].text
        else:
            beds = "0"
        property_obj["beds"].append(beds)

        baths_element = item.find_all("span", attrs={"aria-label": "Baths"})
        if baths_element:
            baths = baths_element[0].text
        else:
            baths = 0
        property_obj["baths"].append(baths)

        property_obj["sqft"].append(item.find_all("span", attrs={"aria-label": "Area"})[0].text)
    df = pandas.DataFrame(property_obj)
    df.to_csv("result.csv", mode="a", header=False, index=False)
