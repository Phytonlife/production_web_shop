# Используем официальный образ Python
FROM python:3.11-slim-bullseye

# Устанавливаем системные зависимости, необходимые для psycopg2 и Pillow
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    jpegoptim \
    libjpeg-dev \
    zlib1g-dev \
    libwebp-dev \
    netcat-openbsd \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код приложения
COPY . /app/

# Делаем скрипт entrypoint исполняемым
RUN chmod +x /app/entrypoint.sh

# Открываем порт, на котором будет работать Gunicorn
EXPOSE 8000

# Определяем команду, которая будет запускаться при старте контейнера
# Используем entrypoint.sh для выполнения миграций и сбора статики
ENTRYPOINT ["/app/entrypoint.sh"]

