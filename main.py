from decouple import config
from telebot import TeleBot

from keyboards import *

token = config('token')
bot = TeleBot(token, 'html')

admin_id = 0

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(user_id, f'Добро пожаловать {name}!\n Выберите свой дом:', reply_markup=get_chats())
    if User.get_or_none(user_id=user_id) is None:
        apt = Apartment.get()
        new = User.create(user_id=user_id, name=name, apt=apt)
        new.save()


@bot.message_handler(func=lambda m: m.text == 'admin tools')
def admin(message):
    global admin_id
    admin_id = message.from_user.id
    bot.send_message(admin_id, 'activated! send apt_id, region, city, type, chat_url\n'
                                    'or entrance, name, floors and apt_on_floor\n splitted with %')

@bot.message_handler(func=lambda m: m.from_user.id == admin_id)
def admin_message(message):
    text = 'ERROR LENTH'
    data = message.text.split('%')
    if len(data) == 4:
        model = Apartment_Type.create(entrance=data[0], name=data[1], floors=data[2], apt_on_floor=data[3])
        model.save()
        text = f'Apartment_Type №{model.id} added'
    elif len(data) == 5:
        apt_type = Apartment_Type.get(id = data[3])
        model = Apartment.create(apt_id=data[0], region=data[1], city=data[2], type=apt_type, chat_url=data[4])
        model.save()
        text = f'Apartment №{model.id} added'
    bot.send_message(admin_id, text)

@bot.callback_query_handler(func=lambda call: call.data.startswith('selected_'))
def test_callback(call):
    user_id = call.message.chat.id
    mag_id = call.message.id
    apt_id = int(call.data.replace('selected_', ''))
    apt = Apartment.get(id=apt_id)

    bot.edit_message_text('Группа вашего дома:', user_id, mag_id, reply_markup=get_chat(apt))
    user = User.select().where(User.user_id==user_id).get()
    user.apt = apt
    user.save()

bot.infinity_polling()
