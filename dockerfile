# Gunakan image Python minimal
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies untuk build (git & pip wheel)
RUN apt-get update && apt-get install -y git && pip install --upgrade pip

# Install library dari GitHub (manual, bukan via requirements.txt)
RUN pip install git+https://github.com/ibm-granite-community/utils.git
RUN pip install langchain_community<0.3.0 replicate Flask==2.2.5

# Salin semua source code
COPY . .

# Jalankan Flask di port Railway (8080)
EXPOSE 8080
CMD ["python", "app.py"]
