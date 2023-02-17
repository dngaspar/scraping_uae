
import requests
from bs4 import BeautifulSoup

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
