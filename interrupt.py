from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from stickers import *


def end(update: Update, context: CallbackContext):
    update.message.reply_photo(
        "https://myslide.ru/documents_7/c2d573d9e648a68842706b978ad351da/img17.jpg",
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def wrong_message(update: Update, context: CallbackContext):
    update.message.reply_sticker(WRONG_COMMAND_STICKER)
    update.message.reply_text('Упс! Такой команды не существует')


def endpoint(update: Update, context: CallbackContext):
    update.message.reply_sticker(ENDPOINT_STICKER)
    update.message.reply_text('Операция прервана')
    return ConversationHandler.END  # завершает диалог о добавлении дела


def delete_message(update: Update, context: CallbackContext, start=0, end=1):
    try:
        for i in range(start, end):
            context.bot.delete_message(update.effective_chat.id,
                                       update.effective_message.message_id - i)  # i = 0, 1, 2, 3, 4
    except:  # если поймаешь ошибки
        pass  # pass




# fruits = [
#     ["Банан", "Яблоко", "Лимон"],
#     ["Банан", "Яблоко", "Лимон"],
#     ["Банан", "Яблоко", "Лимон"]
# ]  # список
# word = "Спидометр"
# prices = {"Симиренко": 74, "Айдаред": 104}
# numbers = range(10)  # диапазон

# for name, price in prices.items():
#     print(f'Цена яблок {name} = {price} рублей', end=" ")
# print()
# for banana, apple, lemon in fruits:
#     print(banana)


# a, b, c = [1, 2, 3]
# print(a)
