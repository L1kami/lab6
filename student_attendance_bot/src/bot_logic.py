# -*- coding: utf-8 -*-
import logging

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start. Надсилає привітання та Telegram ID користувача."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привіт, {user.mention_html()}!\n"
        f"Я бот для відстеження присутності. Ваш Telegram ID: `{user.id}`.\n"
        f"Цей ID можна використовувати в файлі `schedule.xlsx`."
    )


async def handle_presence_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє натискання на inline-кнопку 'Я тут!'.
    """
    query = update.callback_query
    await query.answer()  # Обов'язково, щоб Telegram знав, що запит оброблено

    try:
        # Витягуємо ID уроку з даних кнопки (напр., "confirm_12345:mon:09:00")
        lesson_id = query.data.split("_", 1)[1]
        pending_checks = context.bot_data.get("pending_checks", set())

        if lesson_id in pending_checks:
            # Якщо урок ще очікує підтвердження, видаляємо його зі списку
            pending_checks.discard(lesson_id)
            await query.edit_message_text(text="✅ Дякую, вашу присутність відзначено!")
            logging.info("Учень %s (ID: %s) підтвердив присутність для уроку %s.",
                         query.from_user.full_name, query.from_user.id, lesson_id)
        else:
            # Якщо учень натиснув кнопку запізно або повторно
            await query.edit_message_text(text="☑️ Ваша присутність вже була підтверджена, або час на відповідь вийшов.")

    except (IndexError, AttributeError) as e:
        logging.error("Помилка обробки callback_query: %s. Дані: %s", e, query.data)
        await query.edit_message_text(text="Сталася помилка. Спробуйте ще раз.")

