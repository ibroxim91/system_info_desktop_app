# Python asosli Docker image
FROM python:3.11-slim

# GTK yoki Qt kutubxonalarini o'rnatish uchun kerakli paketlar


# Ishchi papkani sozlash
WORKDIR /app

# Talab qilinadigan Python kutubxonalarini o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani konteynerga ko'chirish
COPY . .

# Flask serverni ishga tushirish
CMD ["python", "main.py"]
