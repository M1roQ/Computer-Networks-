# Используем официальный Python образ
FROM python:3.9-slim

# Установим Firefox и geckodriver
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    curl \
    unzip \
    xauth \
    xvfb \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

# Установка geckodriver (в нужную директорию)
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz" \
    && tar -xvzf geckodriver-v0.36.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.36.0-linux64.tar.gz


# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем весь код проекта
COPY . .

# Открываем порт, чтобы Flask приложение было доступно
EXPOSE 5000

# Запускаем Flask-приложение
CMD ["python", "app.py"]
