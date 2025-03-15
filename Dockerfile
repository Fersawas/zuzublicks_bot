# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порты (если необходимо)
EXPOSE 8080

# Указываем команду для запуска контейнера
CMD ["bash", "-c", "alembic upgrade head && python bot.py"]
