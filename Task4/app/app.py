from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Подключение к PostgreSQL
# Подключение к PostgreSQL с новыми параметрами
def get_db_connection():
    conn = psycopg2.connect(
        host='db',  # имя контейнера с PostgreSQL (db - это имя службы в docker-compose)
        database='parserdb',  # имя базы данных
        user='miro_q',  # новый пользователь
        password='qwerty'  # новый пароль
    )
    return conn


# Функция парсинга и сохранения данных в базу
def parse_and_save(url):
    driver = webdriver.Firefox()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    
    # Пример парсинга: нужно адаптировать под URL и структуру страницы
    products = driver.find_elements(By.CLASS_NAME, 'showcase-item-3')

    conn = get_db_connection()
    cursor = conn.cursor()

    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, 'showcase-name-first').text
            price = product.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
            article = product.find_element(By.CSS_SELECTOR, '.product-code .value').text
            availability = product.find_element(By.CLASS_NAME, 'product-status').text
            link = product.find_element(By.CSS_SELECTOR, 'a[itemprop="url"]').get_attribute('href')
            
            # Вставка в БД
            cursor.execute(
                "INSERT INTO products (name, price, article, availability, link) VALUES (%s, %s, %s, %s, %s)",
                (name, price, article, availability, link)
            )
            conn.commit()
        except Exception as e:
            print("Ошибка при парсинге товара:", e)

    driver.quit()
    cursor.close()
    conn.close()

@app.route('/parse', methods=['GET'])
def parse():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        parse_and_save(url)
        return jsonify({'message': 'Парсинг завершен, данные сохранены в базе'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    # Формируем список продуктов
    product_list = []
    for product in products:
        product_list.append({
            'name': product[0],
            'price': product[1],
            'article': product[2],
            'availability': product[3],
            'link': product[4]
        })

    return jsonify(product_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
