# -*- coding: utf-8 -*-
import asyncio
import logging
from datetime import datetime, time, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from src import scheduler_jobs  # <--- Змінено тут
from src.bot_logic import handle_presence_confirmation, start
from src.config import CONFIRMATION_WINDOW_MINUTES, TELEGRAM_BOT_TOKEN
from src.data_handler import get_schedule_data


def schedule_lessons(scheduler: AsyncIOScheduler, lessons: list, bot_app: Application) -> None:
    """
    Налаштовує та запускає заплановані завдання для кожного уроку з розкладу.
    """
    # Словник для перетворення назв днів тижня у формат, зрозумілий APScheduler
    day_mapping = {
        "Monday": "mon", "Tuesday": "tue", "Wednesday": "wed", "Thursday": "thu",
        "Friday": "fri", "Saturday": "sat", "Sunday": "sun"
    }

    logging.info("Починаю планування %d уроків...", len(lessons))

    for lesson in lessons:
        try:
            day_of_week = day_mapping.get(lesson["lesson_day"])
            if not day_of_week:
                logging.warning("Неправильний день тижня '%s' для учня %s. Пропускаю.",
                                lesson["lesson_day"], lesson["student_name"])
                continue

            lesson_time_obj = datetime.strptime(lesson["start_time"], '%H:%M').time()
            run_time = datetime.combine(datetime.today(), lesson_time_obj)

            job_id_check = f"check_{lesson['student_name']}_{day_of_week}_{lesson['start_time']}"
            job_id_notify = f"notify_{lesson['student_name']}_{day_of_week}_{lesson['start_time']}"

            # Запланувати початкову перевірку присутності
            scheduler.add_job(
                scheduler_jobs.send_presence_check,  # <--- Змінено тут
                'cron',
                day_of_week=day_of_week,
                hour=lesson_time_obj.hour,
                minute=lesson_time_obj.minute,
                id=job_id_check,
                replace_existing=True,
                kwargs={
                    "bot_app": bot_app,
                    "student_id": lesson["student_telegram_id"],
                    "student_name": lesson["student_name"],
                    "job_id": job_id_notify  # Передаємо ID для майбутнього видалення
                }
            )

            # Запланувати перевірку відсутності через N хвилин
            notify_time = run_time + timedelta(minutes=CONFIRMATION_WINDOW_MINUTES)
            scheduler.add_job(
                scheduler_jobs.check_absence_and_notify,  # <--- Змінено тут
                'cron',
                day_of_week=day_of_week,
                hour=notify_time.hour,
                minute=notify_time.minute,
                id=job_id_notify,
                replace_existing=True,
                kwargs={
                    "bot_app": bot_app,
                    "student_id": lesson["student_telegram_id"],
                    "student_name": lesson["student_name"],
                    "teacher_id": lesson["teacher_telegram_id"]
                }
            )
        except (ValueError, KeyError) as e:
            logging.error("Помилка під час планування уроку для %s: %s. Перевірте формат даних.",
                          lesson.get('student_name', 'N/A'), e)

    logging.info("Усі уроки успішно заплановано.")


async def main() -> None:
    """Головна функція для запуску бота."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logging.getLogger("apscheduler").setLevel(logging.WARNING)

    lessons = get_schedule_data()
    if lessons is None:
        logging.critical("Не вдалося завантажити розклад. Роботу бота зупинено.")
        return

    if not lessons:
        logging.warning("Файл з розкладом порожній або не містить коректних даних. Бот працюватиме, але жодних сповіщень не буде.")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_presence_confirmation))

    # Налаштування та запуск планувальника
    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    schedule_lessons(scheduler, lessons, application)
    scheduler.start()

    logging.info("Бот успішно запущений та готовий до роботи.")
    try:
        await application.run_polling()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Роботу бота зупинено.")
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

