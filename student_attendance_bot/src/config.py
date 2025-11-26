# -*- coding: utf-8 -*-
import logging
import os

from dotenv import load_dotenv

# Завантажуємо змінні оточення з .env файлу
load_dotenv()

# --- Головні налаштування ---

# Токен вашого Telegram-бота, який ви отримуєте від @BotFather
# Важливо: цей токен має зберігатися у файлі .env, а не в коді
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    # Якщо токен не знайдено, програма не зможе запуститися
    raise ValueError("Не знайдено TELEGRAM_BOT_TOKEN. Перевірте ваш .env файл.")

# Шлях до файлу Excel з розкладом та списком учнів
# Файл має лежати в кореневій папці проєкту
SCHEDULE_FILE_PATH = "schedule.xlsx"

# Час у хвилинах, який дається учню на підтвердження присутності
CONFIRMATION_WINDOW_MINUTES = 10


# --- Налаштування логування ---

# Рівень логування: INFO - показуватиме основні події, DEBUG - детальна інформація
LOGGING_LEVEL = logging.INFO

# Формат записів у лог
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Встановлюємо базову конфігурацію для логера
logging.basicConfig(
    level=LOGGING_LEVEL,
    format=LOGGING_FORMAT
)

# Зменшуємо кількість логів від сторонніх бібліотек, щоб не засмічувати вивід
logging.getLogger("httpx").setLevel(logging.WARNING)

