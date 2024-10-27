import os
import csv
import jdatetime
import requests
import urllib3
from bs4 import BeautifulSoup
import constants as consts

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Log the start of the script
print("Script started.")

page_numbers = range(1, 3000) 
jalali_now = jdatetime.date.today()
print(f"Current Jalali date: {jalali_now}")

domains = []
break_main = False

for page_number in page_numbers:
    if break_main:
        print("Breaking main loop as per condition.")
        break

    # Log the page being requested
    print(f"Requesting page {page_number}...")

    try:
        response = requests.get(consts.ENAMAD_URL + str(page_number), allow_redirects=True, verify=False)
        response.raise_for_status()
        print(f"Successfully retrieved page {page_number}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve page {page_number}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find("div", class_="table", style="margin-top: 40px;").find_all("div", class_="row")[2:]
    print(f"Found {len(rows)} rows on page {page_number}.")

    for row in rows:
        try:
            md_1 = row.find_all("div", class_="col-md-1")
            md_2 = row.find_all("div", class_="col-md-2")

            id = md_1[0].text.strip()
            enamad = md_2[0].find("a").get("href")
            url = md_2[0].find("a", class_="exlink").get("href")
            title = row.find("div", class_="col-md-3").text.strip()
            province = md_1[1].text.strip()
            city = md_1[2].text.strip()

            stars = len(md_2[1].find_all("img"))
            issued_date = md_1[3].text.strip()
            expire_date = md_1[4].text.strip()

            # Check expiry
            if jdatetime.datetime.strptime(expire_date, '%Y/%m/%d').date() < jalali_now:
                if stars == 1:
                    print("Encountered expired domain with one star; breaking.")
                    break_main = True
                    break
                else:
                    print(f"Skipping expired domain {url} with multiple stars.")
                    continue

            # Log domain details
            print(f"Adding domain: {title} ({url}), Stars: {stars}")

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
        
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

# Sorting the data by domain
print("Sorting domains by 'domain'.")
data = sorted(domains, key=lambda d: d['domain'])

# Ensure directory for CSV output exists
os.makedirs(os.path.dirname(consts.CSV_OUT_PATH), exist_ok=True)

# Write to CSV
print(f"Writing data to {consts.CSV_OUT_PATH}...")
try:
    with open(consts.CSV_OUT_PATH, "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print("Data successfully written to CSV.")
except IOError as e:
    print(f"Failed to write CSV: {e}")

print("Script completed.")
