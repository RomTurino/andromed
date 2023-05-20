from stickers import *
from telegram.ext import (
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler, 
    CallbackContext,
    CallbackQueryHandler
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from constants import *
from interrupt import *
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date



class MyStyleCalendar(DetailedTelegramCalendar):
    # previous and next buttons style. they are emoji now!
    prev_button = "⬅️"
    next_button = "➡️"
    # you do not want empty cells when month and year are being selected
    empty_month_button = ""
    empty_year_button = ""
    middle_button_year = ""


def add_task(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    context.user_data['start_delete'] = update.effective_message.message_id
    update.message.reply_sticker(ADD_STICKER)
    update.message.reply_text(f"Просьба ввести текст дела, мастер {name} или /no чтобы прекратить операцию добавления")
    return TASK

def handle_task_text(update: Update, context: CallbackContext):
    
    message = update.message.text # взяли сообщение, где пользователь пишет текст дела
    context.user_data["todo_text"] = message # сохранили это в рюкзак
    # update.message.reply_text(message)
    calendar, step = MyStyleCalendar(locale="ru", min_date=date.today()).build()
    context.bot.send_message(update.effective_chat.id,
                     f"Выберите {RU_STEP[step]}",
                     reply_markup=calendar)
    return DATE

def handle_date(update: Update, context: CallbackContext):
    result, key, step = MyStyleCalendar(locale="ru", min_date=date.today()).process(update.callback_query.data)
    if not result and key:
        context.bot.send_message(update.effective_chat.id,
                                 f"Выберите {RU_STEP[step]}", reply_markup=key)
    elif result:
        delete_message(update, context, end=3)
        year, month, day = str(result).split('-')
        true_date = day + "." + month + "." + year
        context.bot.send_message(update.effective_chat.id,
                                 f"Вы выбрали {true_date}")
        context.user_data["date"] = true_date # сохранили дату в рюкзак 
        return HOUR
    
    
def handle_hour(update: Update, context: CallbackContext):
    keyboard = []
    steps = {1: 0,
             2: 6,
             3: 12,
             4: 18}
    for line in range(4):
        keyboard.append([])
        for column in range(6):
            keyboard[line].append(InlineKeyboardButton(text=f"{column} + {steps[line-1]}",
                                                       callback_data=f"{column} + {steps[line-1]}"))
    markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        update.effective_chat.id,
        f"Выбери час к которому нужно дело завершить",
        reply_markup=markup,
    )
    
            





add_handler = ConversationHandler(#обработчик диалога
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)],
        DATE: [CallbackQueryHandler(handle_date, DetailedTelegramCalendar.func())]
    },
    fallbacks=[CommandHandler("no", endpoint)]
)