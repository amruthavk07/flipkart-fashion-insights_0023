import time
import re
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


QUERY = "women dress"
BASE_SEARCH = "https://www.flipkart.com/search?q={q}&page={page}"
MAX_PAGES = 100
TARGET_ROWS = 1000
OUT_PATH = Path("data/raw/women_dresses_raw.csv")


def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def extract_card_links(soup):
    """Extract product card links from search page"""
    links = set()
    for a in soup.select('a[href^="/"]'):
        href = a.get("href", "")
        if "/p/" in href and "pid=" in href:
            links.add("https://www.flipkart.com" + href.split("?", 1)[0])
    return list(links)


def text_or_none(node):
    return node.get_text(strip=True) if node else None


def clean_money(txt):
    if not txt:
        return None
    t = re.sub(r"[^0-9.]", "", txt)
    try:
        return float(t)
    except ValueError:
        return None


def extract_product_details(html, url):
    """Extract details from product page"""
    s = BeautifulSoup(html, "html.parser")

    # Product name
    name = text_or_none(s.select_one("span.VU-ZEz")) or \
           text_or_none(s.select_one("span.B_NuCI")) or \
           text_or_none(s.select_one("h1.yhB1nd"))

    # Brand
    brand = text_or_none(s.select_one("span.mEh187")) or \
            text_or_none(s.select_one("span.G6XhRU")) or \
            (name.split()[0] if name else None)

    # Dress subtype
    bc = s.select("a._2whKao")
    dress_type = None
    if bc and len(bc) >= 2:
        dress_type = bc[-1].get_text(strip=True)
    else:
        if name:
            for kw in ["Maxi", "Midi", "A-line", "Fit and Flare", "Bodycon", "Shift", "Gown", "Kaftan"]:
                if kw.lower() in name.lower():
                    dress_type = kw
                    break

    # Prices
    sale_price = text_or_none(s.select_one("div._30jeq3")) or \
                 text_or_none(s.select_one("div.Nx9bqj")) or \
                 text_or_none(s.select_one("div.CxhGGd"))

    mrp = text_or_none(s.select_one("div._3I9_wc")) or \
          text_or_none(s.select_one("div.yRaY8j"))

    # Rating
    rating = text_or_none(s.select_one("div._3LWZlK")) or \
             text_or_none(s.select_one("div.XQDdHH._1Quie7"))

    # Reviews (extract only "Reviews" part)
    reviews_count = None
    rr_text = text_or_none(s.select_one("span._2_R_DZ")) or \
              text_or_none(s.select_one("div.DRxq-P"))
    if rr_text:
        m = re.search(r"([\d,]+)\s+Reviews", rr_text, flags=re.I)
        if m:
            reviews_count = int(m.group(1).replace(",", ""))

    return {
        "Product Name": name,
        "Brand": brand,
        "Category Type": dress_type,
        "MRP (Maximum Retail Price)": clean_money(mrp),
        "Discounted Price / Sale Price": clean_money(sale_price),
        "Rating": float(rating) if rating and re.match(r"^\d+(\.\d+)?$", rating) else None,
        "Number of Reviews": reviews_count,
        "Product URL": url,
    }


def main():
    rows = []
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        for page in range(1, MAX_PAGES + 1):
            if len(rows) >= TARGET_ROWS:
                print(f"✅ Reached target of {TARGET_ROWS} products. Stopping.")
                break

            url = BASE_SEARCH.format(q=QUERY.replace(" ", "+"), page=page)
            driver.get(url)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1AtVbE")))
            except Exception:
                time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = extract_card_links(soup)
            if not links:
                print(f"No results found on page {page}. Stopping.")
                break
            print(f"Page {page}: {len(links)} product links")

            for link in links:
                if len(rows) >= TARGET_ROWS:
                    break
                try:
                    driver.get(link)
                    time.sleep(2)
                    details = extract_product_details(driver.page_source, link)
                    if details:
                        rows.append(details)
                        print(f"[+] {details['Product Name']} | {details['Brand']} | "
                              f"{details['Category Type']} | Reviews: {details['Number of Reviews']}")
                    time.sleep(1.5)
                except Exception as e:
                    print(f"[WARN] Failed {link}: {e}")
                    continue

            time.sleep(2)

    finally:
        driver.quit()

    # ✅ Save only required columns in correct order
    df = pd.DataFrame(rows, columns=[
        "Product Name",
        "Brand",
        "Category Type",
        "MRP (Maximum Retail Price)",
        "Discounted Price / Sale Price",
        "Rating",
        "Number of Reviews",
        "Product URL",
    ])
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"✅ Saved {len(df)} rows -> {OUT_PATH}")


if __name__ == "__main__":
    main()
