import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import psycopg2

# Подключаемся к базе данных PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname="parserdb",
        user="dmitry",
        password="password",
        host="db",  # имя контейнера с базой данных
        port="5432"
    )
    return conn

def save_to_db(data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.executemany("INSERT INTO products (name, price, article, availability, link) VALUES (%s, %s, %s, %s, %s)", data)
    conn.commit()
    cur.close()
    conn.close()

options = Options()
options.headless = True
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

product_data = []

for page in range(1, 5):
    print(f"Парсинг страницы {page}...")

    products = driver.find_elements(By.CLASS_NAME, 'showcase-item-3')

    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, 'showcase-name-first').text
            price = product.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
            article = product.find_element(By.CSS_SELECTOR, '.product-code .value').text
            availability = product.find_element(By.CLASS_NAME, 'product-status').text
            link = product.find_element(By.CSS_SELECTOR, 'a[itemprop="url"]').get_attribute('href')

            product_data.append((name, price, article, availability, link))

            print(f"Добавлен товар: {name}, {price}, {availability}")
        except Exception as e:
            print("Ошибка при парсинге товара:", e)

    try:
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[@href="/catalog/gitari/elektrogitari/?PAGEN_1={page + 1}"]')))
        next_page_button.click()
        time.sleep(3)
    except Exception as e:
        print("Ошибка при переходе на следующую страницу:", e)
        break

# Сохраняем данные в базу
save_to_db(product_data)

driver.quit()
