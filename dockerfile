FROM php:8.2-fpm

# Install dependencies
RUN apt-get update && apt-get install -y \
    git curl zip unzip libonig-dev libxml2-dev libsqlite3-dev sqlite3 \
    && docker-php-ext-install pdo pdo_sqlite mbstring

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Buat folder aplikasi
WORKDIR /var/www

# Copy semua file
COPY . .

# Install dependency Laravel
RUN composer install --no-dev --optimize-autoloader

# Tambah permission dan generate key
RUN chmod -R 777 storage bootstrap/cache

# Salin file env lokal jika belum ada
COPY .env.example .env

# Generate app key
RUN php artisan key:generate

# Jalankan Laravel
CMD php artisan serve --host=0.0.0.0 --port=8080
