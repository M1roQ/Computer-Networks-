import argparse
import time

import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--pages_count", type=int, default=5)
args = parser.parse_args()
max_pages = args.pages_count

conn = psycopg2.connect(
    dbname="products_db",
    user="postgres",
    password="BVal41790",
    host="localhost",
    port="5432"
)
conn.set_client_encoding('UTF8')
cursor = conn.cursor()

options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
driver.get("https://mirm.ru/")
wait = WebDriverWait(driver, 10)

guitar_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Гитары")))
guitar_button.click()
time.sleep(2)

electroguitar_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "ЭЛЕКТРОГИТАРЫ")))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", electroguitar_button)
time.sleep(1)
electroguitar_button.click()
time.sleep(3)

page = 1
while page <= max_pages:
    print(f"Парсинг страницы {page}...")
    products = driver.find_elements(By.CLASS_NAME, 'showcase-item-3')

    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, 'showcase-name-first').text
            price = product.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
            article = product.find_element(By.CSS_SELECTOR, '.product-code .value').text
            availability = product.find_element(By.CLASS_NAME, 'product-status').text
            link = product.find_element(By.CSS_SELECTOR, 'a[itemprop="url"]').get_attribute('href')

            cursor.execute('''
                INSERT INTO products (name, price, article, availability, link)
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, price, article, availability, link))
            conn.commit()

            print(f"Добавлен товар: {name}, {price}, {availability}")
        except Exception as e:
            print("Ошибка при парсинге товара:", e)

    try:
        next_page_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "PAGEN_1=")]'))
        )
        next_page_button.click()
        time.sleep(3)
        page += 1
    except Exception as e:
        print("Ошибка при переходе на следующую страницу или больше страниц нет:", e)
        break

driver.quit()
cursor.close()
conn.close()
