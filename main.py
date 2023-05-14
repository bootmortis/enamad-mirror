import os
import csv

import jdatetime
import requests
import urllib3
from bs4 import BeautifulSoup

import constants as consts

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

page_numbers = range(1, 3000) 

jalali_now = jdatetime.date.today()

domains = []
break_main = False
for page_number in page_numbers:
    if break_main:
        break

    response = requests.get(consts.ENAMAD_URL + str(page_number), allow_redirects=True, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find("div", class_="table", style="margin-top: 40px;").find_all("div", class_="row")[2:]
    for row in rows:
        md_1 = row.find_all("div", class_="col-md-1")
        md_2 = row.find_all("div", class_="col-md-2")
        id = md_1[0].text.strip()
        enamad = md_2[0].find("a").get("href")
        url = md_2[0].find("a", class_="exlink").get("href")
        title = row.find("div", class_="col-md-3").text.strip()
        province = md_1[1].text.strip()
        city = md_1[2].text.strip()

        # count img elements in md_2[1]
        stars = len(md_2[1].find_all("img"))
        issued_date = md_1[3].text.strip()
        expire_date = md_1[4].text.strip()

        if jdatetime.datetime.strptime(expire_date, '%Y/%m/%d').date() < jalali_now:
            if stars == 1:
                break_main = True
                break
            else:
                continue

        domains.append({
            "id": id,
            "enamad": enamad,
            "domain": url,
            "title": title,
            "province": province,
            "city": city,
            "stars": stars,
            "issued_date": issued_date,
            "expire_date": expire_date
        })

data = sorted(domains, key=lambda d: d['domain'])

# make sure directory exists
os.makedirs(os.path.dirname(consts.CSV_OUT_PATH), exist_ok=True)

# Open the CSV file for writing
with open(consts.CSV_OUT_PATH, "w", encoding="utf-8") as csvfile:
    # Create the DictWriter object
    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())

    # Write the column names
    writer.writeheader()

    # Write the data rows
    writer.writerows(data)