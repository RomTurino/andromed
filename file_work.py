from telegram import Update
from telegram.ext import CallbackContext
import os


def init(update:Update, context:CallbackContext):
    username = update.effective_user.username
    file = f'database/{username}.csv'
    if not os.path.exists("database"):# если папки нет
        os.mkdir("database") #то папку создаем
    if not os.path.exists(file):
        open(file, "w") # w - write, открываем файл для записи