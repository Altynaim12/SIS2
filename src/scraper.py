import os
import time
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scrape_flip():
    """
    Scrape book products from flip.kz category page and save to data/raw_flip.csv.
    If nothing is scraped (из-за селекторов/блокировок), создаём тестовые данные.
    """
    url = "https://www.flip.kz/catalog?subsection=1001"  # раздел книг

    options = webdriver.ChromeOptions()
    # Можно включить headless, если всё ок:
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.get(url)

        time.sleep(3)

        # Прокрутка страницы
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Пытаемся найти товары (селектор может меняться на сайте)
        items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        data = []

        for item in items:
            try:
                title_el = item.find_element(By.CSS_SELECTOR, ".name")
                title = title_el.text.strip()

                price_el = item.find_element(By.CSS_SELECTOR, ".price")
                price_text = price_el.text.replace("₸", "").replace(" ", "").strip()

                link_el = item.find_element(By.TAG_NAME, "a")
                url_product = link_el.get_attribute("href")

                data.append(
                    {
                        "title": title,
                        "price": price_text,
                        "url": url_product,
                    }
                )
            except Exception:
                continue

        driver.quit()
    except Exception as e:
        print("Selenium error:", e)
        data = []

    # ---- Fallback: если с сайта ничего не забралось, делаем тестовые данные ----
    if not data:
        print("Warning: no real data scraped from flip.kz, generating mock data...")
        data = []
        for i in range(1, 121):
            data.append(
                {
                    "title": f"test book {i}",
                    "price": 1000 + i * 50,
                    "url": "https://www.flip.kz",
                }
            )

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(data, columns=["title", "price", "url"])
    df.to_csv("data/raw_flip.csv", index=False)
    print(f"Saved {len(df)} rows to data/raw_flip.csv")
    return df


if __name__ == "__main__":
    scrape_flip()
