# Gunakan image python resmi
FROM python:3.10-slim

# Set direktori kerja
WORKDIR /app

# Salin file dependensi
COPY requirements.txt .

# Install dependensi Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Salin semua file ke container
COPY . .

# Jalankan app Flask di port 8080
EXPOSE 8080
CMD ["python", "app.py"]
