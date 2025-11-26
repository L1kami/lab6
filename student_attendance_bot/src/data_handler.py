# -*- coding: utf-8 -*-
import logging
from typing import Dict, List, Optional

import pandas as pd

from src.config import SCHEDULE_FILE_PATH


def get_students_data() -> Optional[Dict[str, int]]:
    """
    Зчитує дані про учнів з аркуша 'Students' у Excel-файлі.

    Повертає словник, де ключ - ім'я учня, а значення - його Telegram ID.
    Якщо виникає помилка, повертає None.
    """
    try:
        # Прямо вказуємо двигун для читання файлу
        df = pd.read_excel(SCHEDULE_FILE_PATH, sheet_name="Students", engine="openpyxl")

        # Перевірка наявності необхідних колонок
        if "student_name" not in df.columns or "telegram_id" not in df.columns:
            logging.error(
                "У файлі '%s' на аркуші 'Students' відсутні обов'язкові колонки "
                "'student_name' або 'telegram_id'.", SCHEDULE_FILE_PATH
            )
            return None

        # Створюємо словник, видаляючи зайві пробіли з імен
        students = df.set_index('student_name')['telegram_id'].to_dict()
        return {str(name).strip(): int(tg_id) for name, tg_id in students.items()}

    except FileNotFoundError:
        logging.error("Файл розкладу '%s' не знайдено. Переконайтеся, що він лежить у кореневій папці проєкту.", SCHEDULE_FILE_PATH)
        return None
    except Exception as e:
        logging.error("Сталася помилка під час читання даних учнів: %s", e, exc_info=True)
        return None


def get_schedule_data() -> Optional[List[Dict]]:
    """
    Зчитує розклад з аркуша 'Schedule' і поєднує його з даними учнів.

    Повертає список уроків у вигляді словників.
    Якщо виникає помилка, повертає None.
    """
    students = get_students_data()
    if not students:
        logging.error("Не вдалося завантажити дані учнів, тому розклад не може бути оброблений.")
        return None

    try:
        # Прямо вказуємо двигун для читання файлу
        df = pd.read_excel(SCHEDULE_FILE_PATH, sheet_name="Schedule", engine="openpyxl")
        required_cols = ["lesson_day", "start_time", "student_name", "teacher_telegram_id"]

        # Перевірка наявності колонок
        if not all(col in df.columns for col in required_cols):
            logging.error("У файлі '%s' на аркуші 'Schedule' відсутні деякі з необхідних колонок: %s.",
                          SCHEDULE_FILE_PATH, required_cols)
            return None

        # Додаємо Telegram ID учня до кожного запису в розкладі
        df['student_telegram_id'] = df['student_name'].str.strip().map(students)

        # Перевірка, чи для всіх учнів з розкладу знайдено ID
        missing_students = df[df['student_telegram_id'].isna()]
        if not missing_students.empty:
            for name in missing_students['student_name'].unique():
                logging.warning("Для учня '%s' з розкладу не знайдено Telegram ID у списку учнів.", name)

        # Видаляємо записи, для яких не вдалося знайти учня
        df.dropna(subset=['student_telegram_id'], inplace=True)

        # Конвертуємо ID в цілочисельний тип
        df['student_telegram_id'] = df['student_telegram_id'].astype(int)
        df['teacher_telegram_id'] = df['teacher_telegram_id'].astype(int)

        return df.to_dict('records')
    except Exception as e:
        logging.error("Сталася помилка під час читання розкладу: %s", e, exc_info=True)
        return None

