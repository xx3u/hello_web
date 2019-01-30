import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


bot = telegram.Bot(token='721528122:AAHx_y2_Xud3Gy784Bspdq8ADk2yP6fc9D8')
print(bot.get_me())
{"first_name": "Alashop.kz", "username": "Alashopkz_bot"}

updater = Updater(token='721528122:AAHx_y2_Xud3Gy784Bspdq8ADk2yP6fc9D8')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def build_menu(buttons, n_cols):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu

def start(bot, update):
    button_list = [
        InlineKeyboardButton("List of Items", callback_data="1"),
        InlineKeyboardButton("New Customer", callback_data="2"),
        InlineKeyboardButton("Add Item", callback_data="3"),
        InlineKeyboardButton("Buy Item", callback_data="4")
    ]
    reply_markup = InlineKeyboardMarkup(
        build_menu(button_list, n_cols=2)
    )
    bot.send_message(chat_id=update.message.chat_id, 
                     text="Alashopkz is a bot for online shop, please select further action.",
                     reply_markup=reply_markup
    )

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
