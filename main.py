import requests
from bs4 import BeautifulSoup
import urllib3

import csv


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Define the URL and page numbers to parse
url = "https://www.enamad.ir/DomainListForMIMT"
page_numbers = range(1, 11) # Change this range to select different pages

# Define the CSV header
csv_header = ["Domain", "Title", "Service", "Star", "State", "City"]

# Create a CSV file and write the header
# with open("enamad_data.csv", "w", encoding="utf-8", newline="") as f:
    # writer = csv.writer(f)
    # writer.writerow(csv_header)

    # Parse each page and extract the required data
    # for page_number in page_numbers:
# page_url = url + str(page_number)
response = requests.get(url, allow_redirects=True, verify=False)
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


    # print all in json
    print({
        "id": id,
        "enamad": enamad,
        "url": url,
        "title": title,
        "province": province,
        "city": city,
        "stars": stars,
        "issued_date": issued_date,
        "expire_date": expire_date
    })

    
    break

        # for item in items:
        #     domain = item.find("div", class_="col-sm-12 col-md-1").get("value")
        #     url = item.find("div", class_="col-sm-12 col-md-2").get("value")
        #     # title = item.find("input", id="txt_title").get("value")
        #     # service = item.find("select", id="drp_service").find("option", selected=True).text.strip()
        #     # star = item.find("select", id="drp_star").find("option", selected=True).text.strip()
        #     # state = item.find("select", id="locationState").find("option", selected=True).text.strip()
        #     # city = item.find("select", id="locationCity").find("option", selected=True).text.strip()
        #     writer.writerow([domain, url])
