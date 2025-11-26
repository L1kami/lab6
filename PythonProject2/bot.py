import sqlite3
import os
import sys
import requests
import pytz
from datetime import datetime, time, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler


# --- Загальні припущення ---
# 1. Присутність: Цей скрипт припускає, що інша система (наприклад,
#    вхід учня в LMS або відмітка вчителя) додає запис у `AttendanceLog`
#    протягом перших 10 хвилин уроку. Цей скрипт лише перевіряє
#    наявність цього запису.
# 2. ID чату: Скрипт припускає, що `Students.parent_chat_id` вже
#    заповнені коректними даними для надсилання сповіщень.
# ---------------------------

class AttendanceManager:
    """
    Інкапсулює логіку моніторингу відвідуваності, перевірки БД
    та надсилання сповіщень через Telegram.
    """

    def __init__(self, db_path: str, bot_token: str):
        """
        Конструктор.

        :param db_path: Шлях до файлу бази даних SQLite3.
        :param bot_token: Токен Telegram-бота.
        """
        self.db_path = db_path
        self.bot_token = bot_token
        print(f"Менеджер ініціалізовано. БД: {self.db_path}")

    def _get_db_connection(self):
        """Приватний метод для підключення до SQLite."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"[ПОМИЛКА БД] Не вдалося підключитися до {self.db_path}: {e}")
            return None

    def _send_telegram_message(self, chat_id: str, message: str):
        """
        Приватний метод для надсилання повідомлень через Telegram API.
        Використовує 'requests' для простоти.
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        try:
            response = requests.post(url, data=payload, timeout=5)
            response.raise_for_status()  # Викличе помилку, якщо статус не 2xx
            print(f"  [Telegram] Повідомлення успішно надіслано до chat_id {chat_id}.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"  [ПОМИЛКА Telegram] Не вдалося надіслати повідомлення до {chat_id}: {e}")
            return False

    def check_and_notify(self, student_id: int, lesson_id: int, lesson_start_str: str):
        """
        Головний метод логіки. Перевіряє відсутність учня та сповіщає батьків.
        Викликається планувальником через 10 хв після початку уроку.
        """
        print(
            f"[ПЕРЕВІРКА] Запуск перевірки для student_id={student_id}, lesson_id={lesson_id} (урок о {lesson_start_str}).")

        conn = self._get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # 1. Отримати дані учня (ім'я, chat_id) та назву уроку
            query_student = """
                SELECT s.full_name, s.parent_chat_id, ls.lesson_name
                FROM Students s
                JOIN LessonsSchedule ls ON s.student_id = ls.student_id
                WHERE s.student_id = ? AND ls.lesson_id = ?
            """
            cursor.execute(query_student, (student_id, lesson_id))
            student_data = cursor.fetchone()

            if not student_data:
                print(f"  [Помилка] Не знайдено учня або урок для student_id={student_id}, lesson_id={lesson_id}.")
                return

            full_name = student_data['full_name']
            parent_chat_id = student_data['parent_chat_id']
            lesson_name = student_data['lesson_name']

            if not parent_chat_id:
                print(
                    f"  [Увага] У учня {full_name} (id={student_id}) не вказано parent_chat_id. Сповіщення неможливе.")
                return

            # 2. Отримати поточну дату (у часовій зоні, як у планувальника)
            today_date = datetime.now(pytz.timezone('Europe/Kyiv')).strftime('%Y-%m-%d')

            # 3. Перевірити, чи є запис про присутність (AttendanceLog)
            # Припускаємо, що запис має бути зроблений ВІД початку уроку ДО моменту перевірки
            lesson_start_dt = datetime.strptime(f"{today_date}T{lesson_start_str}:00", '%Y-%m-%dT%H:%M:%S')

            query_attendance = """
                SELECT 1 FROM AttendanceLog
                WHERE student_id = ? AND lesson_id = ? AND timestamp >= ?
            """
            # Ми перевіряємо, чи є відмітка з моменту початку уроку
            cursor.execute(query_attendance, (student_id, lesson_id, lesson_start_dt.isoformat()))
            attendance_record = cursor.fetchone()

            if attendance_record:
                print(f"  [OK] Учень {full_name} (id={student_id}) присутній на уроці '{lesson_name}'.")
                return

            # 4. Якщо присутності немає, перевірити, чи є поважна причина (AbsenceRecords)
            query_absence = """
                SELECT 1 FROM AbsenceRecords
                WHERE student_id = ? AND date = ?
            """
            cursor.execute(query_absence, (student_id, today_date))
            absence_record = cursor.fetchone()

            if absence_record:
                print(f"  [OK] Учень {full_name} (id={student_id}) відсутній, але є поважна причина.")
                return

            # 5. Якщо присутності немає І поважної причини немає -> НАДІСЛАТИ СПОВІЩЕННЯ
            print(
                f"  [ТРЕК] Учень {full_name} (id={student_id}) відсутній на уроці '{lesson_name}'. Надсилаю сповіщення...")

            message = (
                f"Шановні батьки!\n\n"
                f"Ваша дитина, **{full_name}**, не з'явилася на уроці **'{lesson_name}'**, що розпочався о {lesson_start_str}.\n\n"
                f"Ми не отримували від вас повідомлення про поважну причину відсутності на сьогодні ({today_date}).\n\n"
                f"Будь ласка, зв'яжіться з класним керівником."
            )

            self._send_telegram_message(parent_chat_id, message)

        except sqlite3.Error as e:
            print(f"[ПОМИЛКА БД] Помилка під час check_and_notify: {e}")
        finally:
            if conn:
                conn.close()


def setup_database():
    """
    Створює (якщо не існує) таблиці БД та наповнює їх тестовими даними.
    """
    print("[Setup] Налаштування бази даних 'attendance.db'...")
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Створення таблиць
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        parent_chat_id TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LessonsSchedule (
        lesson_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        lesson_name TEXT NOT NULL,
        start_time TEXT NOT NULL, -- Формат "HH:MM"
        day_of_week INTEGER NOT NULL, -- 0=Пн, 1=Вт, ..., 6=Нд
        FOREIGN KEY (student_id) REFERENCES Students (student_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AttendanceLog (
        log_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        lesson_id INTEGER,
        timestamp TEXT NOT NULL, -- ISO 8601
        FOREIGN KEY (student_id) REFERENCES Students (student_id),
        FOREIGN KEY (lesson_id) REFERENCES LessonsSchedule (lesson_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AbsenceRecords (
        absence_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        date TEXT NOT NULL, -- Формат "YYYY-MM-DD"
        reason TEXT,
        FOREIGN KEY (student_id) REFERENCES Students (student_id)
    )
    ''')

    # Наповнення тестовими даними
    # ВАЖЛИВО: Замініть 'YOUR_PARENT_CHAT_ID' на ваш реальний chat_id для тестів
    # Щоб дізнатися свій chat_id, напишіть боту @userinfobot
    test_chat_id = 'YOUR_PARENT_CHAT_ID'  # <-- ЗАМІНІТЬ ЦЕ

    try:
        # Учні
        cursor.execute("INSERT OR IGNORE INTO Students (student_id, full_name, parent_chat_id) VALUES (?, ?, ?)",
                       (101, 'Іваненко Петро', test_chat_id))
        cursor.execute("INSERT OR IGNORE INTO Students (student_id, full_name, parent_chat_id) VALUES (?, ?, ?)",
                       (102, 'Сидоренко Марія', test_chat_id))
        cursor.execute("INSERT OR IGNORE INTO Students (student_id, full_name, parent_chat_id) VALUES (?, ?, ?)",
                       (103, 'Коваленко Андрій', '12345678'))  # Інший ID для демонстрації

        # Поточний день тижня (0=Пн, ..., 6=Нд)
        tz = pytz.timezone('Europe/Kyiv')
        today_weekday = datetime.now(tz).weekday()

        # Видаляємо старий розклад на сьогодні
        cursor.execute("DELETE FROM LessonsSchedule WHERE day_of_week = ?", (today_weekday,))

        # Час для тестування: беремо поточний час + 11 хвилин
        # (1 хвилина на запуск + 10 хвилин очікування)
        test_time = (datetime.now(tz) + timedelta(minutes=11)).strftime('%H:%M')

        print(f"[Setup] Сьогодні {datetime.now(tz).strftime('%A')} (day_of_week={today_weekday}).")
        print(f"[Setup] Додано тестовий урок на {test_time} для перевірки негайного запуску.")

        # Уроки на сьогодні
        # Сценарій 1: Учень 101, відсутній (для нього немає записів)
        cursor.execute(
            "INSERT INTO LessonsSchedule (student_id, lesson_name, start_time, day_of_week) VALUES (?, ?, ?, ?)",
            (101, 'Математика', test_time, today_weekday))  # 101, Математика, <через 11 хв>

        # Сценарій 2: Учень 102, відсутній, але є поважна причина
        cursor.execute(
            "INSERT INTO LessonsSchedule (student_id, lesson_name, start_time, day_of_week) VALUES (?, ?, ?, ?)",
            (102, 'Фізика', test_time, today_weekday))  # 102, Фізика, <через 11 хв>

        today_date_str = datetime.now(tz).strftime('%Y-%m-%d')
        cursor.execute("INSERT OR IGNORE INTO AbsenceRecords (student_id, date, reason) VALUES (?, ?, ?)",
                       (102, today_date_str, 'За сімейними обставинами'))

        # Сценарій 3: Учень 103, присутній (для нього буде запис у AttendanceLog)
        # Додаємо урок
        res = cursor.execute(
            "INSERT INTO LessonsSchedule (student_id, lesson_name, start_time, day_of_week) VALUES (?, ?, ?, ?)",
            (103, 'Англійська', test_time, today_weekday))  # 103, Англійська, <через 11 хв>
        lesson_id_103 = res.lastrowid

        # Імітуємо, що він "відмітився"
        cursor.execute("INSERT INTO AttendanceLog (student_id, lesson_id, timestamp) VALUES (?, ?, ?)",
                       (103, lesson_id_103, datetime.now(tz).isoformat()))

        conn.commit()
        print("[Setup] Базу даних налаштовано з тестовими даними.")
    except sqlite3.Error as e:
        print(f"[ПОМИЛКА БД] Помилка під час налаштування БД: {e}")
        conn.rollback()
    finally:
        conn.close()


def schedule_daily_checks(manager: AttendanceManager, scheduler):
    """
    Запитує уроки на *поточний* день і планує для них завдання перевірки.
    """
    try:
        # Визначаємо часову зону та поточний день
        tz = pytz.timezone('Europe/Kyiv')
        now = datetime.now(tz)
        today_weekday = now.weekday()  # 0=Пн, ..., 6=Нд

        print(
            f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Запуск `schedule_daily_checks` на {now.strftime('%A')} (day={today_weekday})...")

        conn = manager._get_db_connection()
        if not conn:
            print("[ПОМИЛКА] Не вдалося підключитися до БД для планування.")
            return

        cursor = conn.cursor()

        # 1. Запитуємо всі уроки на сьогодні
        query = "SELECT lesson_id, student_id, lesson_name, start_time FROM LessonsSchedule WHERE day_of_week = ?"
        cursor.execute(query, (today_weekday,))
        todays_lessons = cursor.fetchall()
        conn.close()

        if not todays_lessons:
            print("  [Планувальник] На сьогодні уроків у розкладі немає.")
            return

        print(f"  [Планувальник] Знайдено {len(todays_lessons)} уроків на сьогодні.")

        # 2. Створюємо завдання для кожного уроку
        jobs_added = 0
        for lesson in todays_lessons:
            try:
                lesson_id = lesson['lesson_id']
                student_id = lesson['student_id']
                lesson_name = lesson['lesson_name']
                start_time_str = lesson['start_time']  # "HH:MM"

                # Парсимо час
                lesson_time = time.fromisoformat(start_time_str)

                # Розраховуємо час перевірки (початок + 10 хвилин)
                run_dt = datetime.combine(now.date(), lesson_time, tzinfo=tz) + timedelta(minutes=10)

                # Не плануємо завдання, якщо час перевірки вже минув
                if run_dt < now:
                    print(
                        f"    - Пропущено: Урок '{lesson_name}' (id={lesson_id}) о {start_time_str}. Час перевірки ({run_dt.strftime('%H:%M')}) вже минув.")
                    continue

                # Додаємо завдання
                job_id = f"check_{today_weekday}_{lesson_id}_{student_id}"
                scheduler.add_job(
                    manager.check_and_notify,
                    'date',
                    run_date=run_dt,
                    args=[student_id, lesson_id, start_time_str],
                    id=job_id,
                    replace_existing=True  # Замінюємо, якщо завдання вже є
                )
                print(
                    f"    + ЗАПЛАНОВАНО: Урок '{lesson_name}' (id={lesson_id}) о {start_time_str}. Перевірка о {run_dt.strftime('%H:%M:%S')}.")
                jobs_added += 1

            except Exception as e:
                print(f"    [ПОМИЛКА] Не вдалося запланувати job для lesson_id={lesson.get('lesson_id')}: {e}")

        print(f"  [Планувальник] Успішно додано {jobs_added} завдань.")

    except Exception as e:
        print(f"[КРИТИЧНА ПОМИЛКА] в `schedule_daily_checks`: {e}")


def main():
    """
    Головна функція запуску.
    """
    print("Запуск сервісу моніторингу відвідуваності...")

    # 4. 🔒 Точка входу та Безпека
    BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

    if not BOT_TOKEN:
        print("=" * 50)
        print("ПОМИЛКА: Не знайдено змінну оточення 'TELEGRAM_BOT_TOKEN'.")
        print("Будь ласка, встановіть її перед запуском:")
        print("  Linux/macOS: export TELEGRAM_BOT_TOKEN='ваш_токен'")
        print("  Windows (cmd): set TELEGRAM_BOT_TOKEN='ваш_токен'")
        print("  Windows (PowerShell): $env:TELEGRAM_BOT_TOKEN='ваш_токен'")
        print("=" * 50)
        sys.exit(1)

    # Створюємо та наповнюємо БД тестовими даними
    setup_database()

    # Ініціалізуємо менеджер
    manager = AttendanceManager('attendance.db', BOT_TOKEN)

    # 3. 🗓️ Планувальник завдань
    tz = pytz.timezone('Europe/Kyiv')
    scheduler = BlockingScheduler(timezone=tz)

    # Додаємо головне завдання: запускати `schedule_daily_checks` щодня о 00:01
    scheduler.add_job(
        schedule_daily_checks,
        'cron',
        hour=0,
        minute=1,
        args=[manager, scheduler],
        id='daily_scheduler_job'
    )
    print(f"[Планувальник] Завдання `schedule_daily_checks` заплановано на щоденне виконання о 00:01 (Час: {tz}).")

    # Викликаємо `schedule_daily_checks` один раз вручну при старті
    # (запускаємо в 'date' через 2 секунди, щоб дати час на ініціалізацію)
    scheduler.add_job(
        schedule_daily_checks,
        'date',
        run_date=datetime.now(tz) + timedelta(seconds=2),
        args=[manager, scheduler],
        id='initial_run_job'
    )

    try:
        print("\n" + "=" * 50)
        print(f"Сервіс запущено о {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')}. Очікування на завдання...")
        print("Натисніть Ctrl+C для виходу.")
        print("=" * 50 + "\n")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nЗупинка сервісу...")
        scheduler.shutdown()
        print("Сервіс зупинено.")


if __name__ == "__main__":
    main()