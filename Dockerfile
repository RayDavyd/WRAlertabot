FROM python:3.12-slim

# Instala dependências do sistema (necessário pro pyproj)
RUN apt-get update && apt-get install -y \
    libproj-dev \
    proj-bin \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
