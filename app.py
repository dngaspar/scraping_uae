import re
import threading
import concurrent.futures

import requests
import pandas
from bs4 import BeautifulSoup
from soupsieve import purge


off_plan_param = "?completion_status=off-plan"
ready_plan_param = "?completion_status=ready"
def get_soup(_text):
        return BeautifulSoup(_text, features="html.parser")

def fetch_property(link, category):
    try:
        url = f"https://www.bayut.com{link}"
        resp = requests.get(url)
        soup = get_soup(resp.text)
        price = soup.find_all("span", attrs={"aria-label": "Price"})[0].text
        if category == "to-rent":
            frequency = soup.find_all("span", attrs={"aria-label": "Frequency"})[0].text
        # try:
        beds = soup.find_all("span", attrs={"aria-label": "Beds"})[0].text
        # except:
        #     beds = soup.find_all("span", attrs={"aria-label": "Beds"})[0].text
        baths = soup.find_all("span", attrs={"aria-label": "Baths"})[0].text
        area = soup.find_all("span", attrs={"aria-label": "Area"})[0].text

        type = soup.find_all("span", attrs={"aria-label": "Type"})[0].text
        purpose = soup.find_all("span", attrs={"aria-label": "Purpose"})[0].text
        reference_no = soup.find_all("span", attrs={"aria-label": "Reference"})[0].text
        try:
            furnishing = soup.find_all("span", attrs={"aria-label": "Furnishing"})[0].text
        except:
            furnishing = ""
        try:
            trucheck_date = soup.find_all("span", attrs={"aria-label": "Trucheck date"})[0].text
        except:
            trucheck_date = ""
        try:
            addon_data = soup.find_all("span", attrs={"aria-label": "Reactivated date"})[0].text
        except:
            addon_data = ""
        try:
            developer = soup.find_all("span", attrs={"aria-label": "Developer"})[0].text
        except:
            developer = ""
        try:
            ownership = soup.find_all("span", attrs={"aria-label": "Ownership"})[0].text
        except:
            ownership = ""
        try:
            built_up_area = soup.find_all("span", attrs={"aria-label": "Built-up Area"})[0].text
        except:
            built_up_area = ""
        try:
            usage = soup.find_all("span", attrs={"aria-label": "Usage"})[0].text
        except:
            usage = ""
        try:
            balcony_size = soup.find_all("span", attrs={"aria-label": "Balcony Size"})[0].text
        except:
            balcony_size = ""
        try:
            parking = soup.find_all("span", attrs={"aria-label": "Parking Availability"})[0].text
        except:
            parking = ""
        try:
            location = soup.find_all("div", attrs={"aria-label": "Property header"})[0].text
            city = location.split(",")[-1]
            building = ", ".join(location.split(",")[:-3])
            location = location.split(",")[-2]
        except:
            city = ""
            building = ""
            location = ""
        # except:
        #     return False
        

        response = {
            "price": price,
            "city": city,
            "location": location,
            "building": building,
            "beds": beds,
            "baths": baths,
            "area": area,
            "type": type,
            "purpose": purpose,
            "reference_no": reference_no,
            "furnishing": furnishing,
            "trucheck": trucheck_date,
            "added_on": addon_data,
            "developer": developer,
            "ownership": ownership,
            "built_up_area": built_up_area,
            "usage": usage,
            "balcony_size": balcony_size,
            "parking_availability": parking,
            "link": url
        }
        if category == "to-rent":
            response["frequency"] = frequency
        return response
    except:
        return False


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
        resp = requests.get(url)
        soup = get_soup(resp.text)
        li_tag_list = soup.find_all("li", attrs={"role": "article"})
        property_obj = {
            "price": [],
            "city": [],
            "location": [],
            "building": [],
            "beds": [],
            "baths": [],
            "area": [],
            "type": [],
            "purpose": [],
            "reference_no": [],
            "furnishing": [],
            "trucheck": [],
            "added_on": [],
            "developer": [],
            "ownership": [],
            "built_up_area": [],
            "usage": [],
            "balcony_size": [],
            "parking_availability": [],
            "link": []
        }
        if category == "to-rent":
            property_obj["frequency"] = []
        if not li_tag_list:
            break
        link_list = []
        for item in li_tag_list:
            link = item.find_all("a", attrs={"aria-label": "Listing link"})[0]["href"]
            link_list.append(link)
        
        thread_pool_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for link in link_list:
                thread_pool_list.append(executor.submit(fetch_property, link, category))
            for item in thread_pool_list:
                for key in property_obj.keys():
                    if item.result():
                        property_obj[key].append(item.result()[key])


        df = pandas.DataFrame(property_obj)
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