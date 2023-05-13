from stickers import *
from telegram.ext import (
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler, 
    CallbackContext
)
from telegram import Update
from constants import *



from datetime import date

def add_task(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    update.message.reply_sticker(ADD_STICKER)
    update.message.reply_text(f"Просьба ввести текст дела, мастер {name} или /no чтобы прекратить операцию добавления")
    return TASK

def handle_task_text(update: Update, context: CallbackContext):
    message = update.message.text # взяли сообщение, где пользователь пишет текст дела
    context.user_data["todo_text"] = message # сохранили это в рюкзак
    update.message.reply_text(message)
    

def endpoint(update: Update, context: CallbackContext):
    update.message.reply_sticker(ENDPOINT_STICKER)
    update.message.reply_text('Операция прервана')
    return ConversationHandler.END # завершает диалог о добавлении дела


add_handler = ConversationHandler(#обработчик диалога
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)]
    },
    fallbacks=[CommandHandler("no", endpoint)]
)