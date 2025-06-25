#!/bin/bash

# --- Проверка наличия необходимых инструментов ---
echo "=== Проверяю наличие необходимых инструментов ==="

# Проверка VirtualBox
if ! command -v virtualbox &> /dev/null; then
    echo "Ошибка: VirtualBox не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "VirtualBox установлен."
fi

# Проверка Ansible
if ! command -v ansible &> /dev/null; then
    echo "Ошибка: Ansible не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "Ansible установлен."
fi

# Проверка Python3
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python3 не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "Python3 установлен."
fi

# Проверка npm
if ! command -v npm &> /dev/null; then
    echo "Ошибка: npm не установлен. Установите его и повторите попытку."
    exit 1
else
    echo "npm установлен."
fi

# --- Проверка содержимого папки images ---
echo "=== Проверяю папку images ==="

# Список ожидаемых файлов
expected_files=("ActiveDirectory.ova" "Kali.ova" "Mikrotik.ova" "Ubuntu_Server.ova")

# Проверяем каждую директорию
for file in "${expected_files[@]}"; do
    if [ ! -f "images/$file" ]; then
        echo "Ошибка: Файл $file не найден в папке images."
        exit 1
    fi
done

echo "Все необходимые файлы в папке images найдены."

# --- Настройка и запуск фронтенда ---
echo "=== Настраиваю фронтенд ==="

# Переход в папку frontend/src
cd frontend/src || { echo "Ошибка: Папка frontend/src не найдена"; exit 1; }

# Установка зависимостей через npm
echo "Устанавливаю зависимости для фронтенда..."
npm install || { echo "Ошибка: Не удалось установить зависимости для фронтенда"; exit 1; }

# Запуск фронтенда в фоновом режиме
echo "Запускаю фронтенд..."
npm start &

# Возвращаемся в корень проекта
cd ../..

# --- Настройка и запуск бэкенда ---
echo "=== Настраиваю бэкенд ==="

# Переход в папку backend
cd backend || { echo "Ошибка: Папка backend не найдена"; exit 1; }

# Создание виртуального окружения Python
echo "Создаю виртуальное окружение для бэкенда..."
python3 -m venv venv || { echo "Ошибка: Не удалось создать виртуальное окружение"; exit 1; }

# Активация виртуального окружения
echo "Активирую виртуальное окружение..."
source venv/bin/activate || { echo "Ошибка: Не удалось активировать виртуальное окружение"; exit 1; }

# Установка зависимостей из requirements.txt
echo "Устанавливаю зависимости для бэкенда..."
pip install -r requirements.txt || { echo "Ошибка: Не удалось установить зависимости для бэкенда"; exit 1; }

# Инициализация миграций (если каталог migrations еще не создан)
if [ ! -d "migrations" ]; then
    echo "Инициализирую директорию миграций..."
    flask db init || { echo "Ошибка: Не удалось инициализировать директорию миграций"; exit 1; }
fi

# Генерация миграции
echo "Генерирую скрипт миграции..."
flask db migrate -m "Initial migration." || { echo "Ошибка: Не удалось сгенерировать миграцию"; exit 1; }

# Применение миграций
echo "Применяю миграции к базе данных..."
flask db upgrade || { echo "Ошибка: Не удалось применить миграции"; exit 1; }

# Переход в подпапку backend/src
cd src || { echo "Ошибка: Папка backend/src не найдена"; exit 1; }

# Запуск скрипта init_db.py
echo "Запускаю скрипт init_db.py для инициализации базы данных..."
python3 init_db.py || { echo "Ошибка: Не удалось выполнить init_db.py"; exit 1; }

# Запуск Python-приложения
echo "Запускаю бэкенд..."
python3 app.py || { echo "Ошибка: Не удалось запустить бэкенд"; exit 1; }