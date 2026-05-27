# Используем официальный легковесный образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости, необходимые для pygame и сборки
RUN apt-get update && apt-get install -y \
    make \
    gcc \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-setuptools \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Задаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код проекта в контейнер
COPY . .

# Команда по умолчанию (будет переопределяться в docker-compose)
CMD ["python", "main.py"]
