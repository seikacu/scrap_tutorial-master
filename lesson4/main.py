# This is the way
# Author: pythontoday
# YouTube: https://www.youtube.com/c/PythonToday/videos

import requests
from bs4 import BeautifulSoup
from proxy_auth import proxies
import json


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

# collect all fests URLs
fests_urls_list = []
# for i in range(0, 216, 24):
for i in range(0, 24, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&where[]=2&where[]=3&where[]=4&maxprice=500&o={i}&bannertitle=June"
    # print(url)
    
    req = requests.get(url=url, headers=headers) # proxies=proxies
    json_data = json.loads(req.text)
    html_response = json_data["html"]

    with open(f"lesson4/data/index_{i}.html", "w") as file:
        file.write(html_response)

    with open(f"lesson4/data/index_{i}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all("a", class_="card-details-link")

    for item in cards:
        fest_url = "https://www.skiddle.com" + item.get("href")
        fests_urls_list.append(fest_url)

# print(fests_urls_list)

# # collect fest info
# count = 0
# fest_list_result = []
for url in fests_urls_list:
#     count += 1
#     print(count)
#     print(url)

    req = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(req.text, "lxml")
        fest_info_block = soup.find("div", class_="MuiContainer-root")
        fest_info_block2 = soup.find("div", class_="MuiPaper-root")
        fest_info_block2_list = fest_info_block2.find_all("span")
               
        fest_name = fest_info_block.find("h1").text.strip()
        fest_date = fest_info_block2_list[0].text.strip() + ', ' + fest_info_block2_list[1].text.strip()
        location = fest_info_block2_list[2].text.strip()
        print(fest_name)
        print(fest_date)
        print(location)
        print("#" * 20)
        
#         fest_location_url = "https://www.skiddle.com" + fest_info_block.find("a", class_="tc-white").get("href")

#         # get contact details and info
#         req = requests.get(url=fest_location_url, headers=headers)
#         soup = BeautifulSoup(req.text, "lxml")

#         contact_details = soup.find("h2", string="Venue contact details and info").find_next()
#         items = [item.text for item in contact_details.find_all("p")]

#         contact_details_dict = {}
#         for contact_detail in items:
#             contact_detail_list = contact_detail.split(":")

#             if len(contact_detail_list) == 3:
#                 contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip() + ":"\
#                                                                        + contact_detail_list[2].strip()
#             else:
#                 contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip()

#         fest_list_result.append(
#             {
#                 "Fest name": fest_name,
#                 "Fest date": fest_date,
#                 "Contacts data": contact_details_dict
#             }
#         )

    except Exception as ex:
        print(ex)
        print("Damn...There was some error...")

# with open("fest_list_result.json", "a", encoding="utf-8") as file:
#     json.dump(fest_list_result, file, indent=4, ensure_ascii=False)
