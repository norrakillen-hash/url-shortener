# Берем официальный образ Python (не самый новый, для стабильности)
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем сначала только requirements.txt (для кэширования слоев)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . .

# Команда для запуска (без --reload, так как это прод-режим)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
