import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

LISTING_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (Richfield Data Science 500 student project)"}

def get_soup(url, session):
    response = session.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")

def parse_detail_page(url, session):
    soup = get_soup(url, session)
    category = soup.select("ul.breadcrumb li a")[2].text.strip()
    desc_header = soup.find("div", id="product_description")
    description = (
        desc_header.find_next_sibling("p").text.strip() if desc_header else None
    )

    info = {
        row.th.text.strip(): row.td.text.strip()
        for row in soup.select("table.table-striped tr")
    }

    availability = info.get("Availability", "")
    match = re.search(r"\((\d+) available\)", availability)
    quantity = int(match.group(1)) if match else None

    return {
        "Category": category,
        "Description": description,
        "UPC": info.get("UPC"),
        "Num_Reviews": info.get("Number of reviews"),
        "Stock_Quantity": quantity,
    }

def scrape_books(max_pages=50, delay=0.2):
    books = []
    session = requests.Session()

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}/{max_pages}")
        page_url = LISTING_URL.format(page)
        soup = get_soup(page_url, session)

        for book in soup.find_all("article", class_="product_pod"):
            record = {
                "Title": book.h3.a["title"],
                "Price": book.find("p", class_="price_color").text.strip(),
                "Rating": book.find("p", class_="star-rating")["class"][1],
                "Stock": book.find("p", class_="availability").text.strip(),
            }

            detail_url = urljoin(page_url, book.h3.a["href"])
            try:
                record.update(parse_detail_page(detail_url, session))
            except Exception as e:
                print(f"  Could not read detail page for '{record['Title']}': {e}")

            books.append(record)
            time.sleep(delay)

    df = pd.DataFrame(books)
    df.to_csv("raw_books.csv", index=False)
    print(f"Raw dataset saved: {len(df)} books.")
    return df

df_raw = scrape_books()
df_raw.head()