import os
import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from playhouse.shortcuts import model_to_dict, dict_to_model

from models import Item, Customer, Cart, CartItem
from models import db

token = os.environ['BOT_TOKEN']
bot = telegram.Bot(token=token)
print(bot.get_me())
{"first_name": "Alashop.kz", "username": "Alashopkz_bot"}

updater = Updater(token=token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)



#def build_menu(buttons, n_cols):
#    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#    return menu

def start(bot, update):
#    button_list = [
#        InlineKeyboardButton('List of Items', url='https://getbootstrap.com/docs/4.2/layout/utilities-for-layout/', callback_data="1"),
#        InlineKeyboardButton('New Customer', callback_data="1"),
#        InlineKeyboardButton('Add Item', callback_data="1"),
#        InlineKeyboardButton('Buy Item', callback_data="1")
#    ]
#    reply_markup = InlineKeyboardMarkup(
#        build_menu(button_list, n_cols=2)
#    )
    bot.send_message(chat_id=update.message.chat_id, 
                     text='Alashopkz is a bot for online shopping, welcome on board!'
                     '\nWe have guidance for you.'
                     '\nIf you want to review our list of items, please use /items'
                     '\nIf you want to register, please use /customer Your name Your age'
                     '\nIf you want to add to cart, please use /add Your name Item name'
                     '\nIf you want to go to Your Cart, please use /cart'
                     '\nIf you want to buy, please use /buy')
    

def items(bot, update, args):
    try:
        items = Item.select()
        bot.send_message(
            chat_id=update.message.chat_id,
            text='{}'.format(item.items)
            )

    except Exception as e:
        logging.error(e, exc_info=True)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Fail {}'.format(e)
        )


def customer(bot, update, args):
    try:
        name = args[0]
        age = args[1]
        customer = Customer(
            name=name,
            age=age
            )
        customer.save()
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Congratulations, {}! You are registered and can continue shopping :)'
            .format(name)
            )

    except Exception as e:
        logging.error(e, exc_info=True)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Fail {}'.format(e)
        )


def add(bot, update, args):
    try:
        if len(args) == 2:
            customer_name = args[0]
            customer = Customer.select().where(
                Customer.name == customer_name
            )[0]
            logging.INFO('error')
        else:
            item_name = args[0]
            item = Item.select().where(Item.name == item_name)[0]
            cart = Cart(
                customer=customer
            )
            cart.save()
            cart_item = CartItem(
                cart=cart,
                item=item,
                quantity=quantity
            )
            cart_item.save()
            bot.send_message(
                chat_id=update.message.chat_id,
                text='{}, thanks for shopping with us. Item: {} added to Your Cart.'.
                format(cart.customer, cart_item.item)
            )
    except Exception as e:
        logging.error(e, exc_info=True)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Fail {}'.format(e)
        )

def cart(bot, update, args):
    pass



   
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


start_handler = CommandHandler('start', start)
items_handler = CommandHandler('items', items)
customer_handler = CommandHandler('customer', customer, pass_args=True)
add_handler = CommandHandler('add', add, pass_args=True)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(items_handler)
dispatcher.add_handler(customer_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(echo_handler)


updater.start_polling()
