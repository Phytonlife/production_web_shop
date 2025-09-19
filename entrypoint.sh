#!/bin/sh

# Ожидаем, пока база данных станет доступной
# Это важно, чтобы Django не пытался подключиться к еще не запущенной БД
until nc -z db 5432; do
  echo "Waiting for db to be ready..."
  sleep 2
done

echo "Db is ready!"

# Применяем миграции базы данных
python manage.py migrate

# Собираем статические файлы
python manage.py collectstatic --noinput

# Запускаем Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
