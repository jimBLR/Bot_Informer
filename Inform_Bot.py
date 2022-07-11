import telebot
from telebot import types
from templates.config import BOT_TOKEN
from templates.weather import get_weather
from templates.translate import *
from templates.parser import *
from templates.news import get_article
from templates.world_time import time_world
import requests

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
translator = Translator()


@bot.message_handler(commands=['start'])
def command_start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton('Help ⚹')
    btn2 = types.KeyboardButton('Translate ⇄')
    btn3 = types.KeyboardButton('Parser ⬇')
    btn4 = types.KeyboardButton('Weather 🔆')
    btn5 = types.KeyboardButton('World Time ⏳')
    btn6 = types.KeyboardButton('News 🗞')
    btn7 = types.KeyboardButton('Hide Keyboard ✖')
    start_markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, f' Добро пожаловать 👋 {message.from_user.first_name}!\n'
                                      f'Я - {bot.get_me().first_name} бот!')
    bot.send_message(message.from_user.id, "Чтобы спрятать меню,нажмте 'Hide Keyboard'", reply_markup=start_markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Hide Keyboard ✖':
            hide = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, '...', reply_markup=hide)

        elif message.text == 'Help ⚹':
            bot.send_message(message.chat.id, "Weather - актуальная погода\n"
                                              "World time - мировое время\n"
                                              "News - мировая новость\n"
                                              "Parser  - парсинг б/у автомобилей\n"
                                              "Translate - Google переводчик")
        elif message.text == 'Parser ⬇':
            try:
                sent = bot.send_message(message.chat.id, 'Здравствуйте. Я помогу Вам с парсингом автомобилей с сайта \n'
                                                         'https://cars.av.by\n'
                                                         'Для получения списка б/у машин отправьте ссылку '
                                                         f'формата:\n '
                                                         f'https://cars.av.by/cars/model\n'
                                                         f'Например : https://cars.av.by/bmw/x6')

                bot.register_next_step_handler(sent, parse, )

            except requests.exceptions.MissingSchema:
                bot.send_message(message.chat.id, "Не верный ввод,попробуйте еще раз!")

        elif message.text == 'Weather 🔆':
            sent = bot.send_message(message.chat.id, "Введите название своего города!\n"
                                                     "Пример :  Minsk или Минск")
            bot.register_next_step_handler(sent, send_weather)

        elif message.text == 'World Time ⏳':
            sent = bot.send_message(message.chat.id, "Введите название своего города или страны !\n"
                                                     "Пример :  Moscow( Москва)  or  China(Китай)")
            bot.register_next_step_handler(sent, send_time)
        elif message.text == 'News 🗞':
            bot.send_message(message.chat.id, "Свежа я новость из BBC:\n")
            bot.send_message(message.chat.id, get_article(), parse_mode='HTML')

        elif message.text == 'Translate ⇄':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn8 = types.KeyboardButton('English')
            btn9 = types.KeyboardButton('German')
            btn10 = types.KeyboardButton('Polish')
            btn11 = types.KeyboardButton('Spanish')
            btn12 = types.KeyboardButton('French')
            back = types.KeyboardButton('Назад')
            markup.add(btn8, btn9, btn10, btn11, btn12, back)

            sent = bot.send_message(message.chat.id, 'Выберите язык на который хотите перевести!'
                                                     'После нажмите "Hазад", чтобы вернуться в меню выбора',
                                    reply_markup=markup)
            bot.register_next_step_handler(sent, get_input)
        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Help ⚹')
            btn2 = types.KeyboardButton('Translate ⇄')
            btn3 = types.KeyboardButton('Parser ⬇')
            btn4 = types.KeyboardButton('Weather 🔆')
            btn5 = types.KeyboardButton('World Time ⏳')
            btn6 = types.KeyboardButton('News 🗞')
            btn7 = types.KeyboardButton('Hide Keyboard ✖')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

            bot.send_message(message.chat.id, 'Возвращаемся', reply_markup=markup)


def parse(message):
    html = get_html(URL)
    if html.status_code == 200:
        car_list = []
        if islink(message.text):
            for page in range(1, ):
                html = get_html(message.text, params={'page': page})
                car_list.extend(get_content(html.text))
                save_file(car_list, '../cars.xlsx')
                file = open('../cars.xlsx')
                bot.send_message(message.chat.id, f'Вот Ваша ссылка для скачивания списка автомобилей!')
                bot.send_document(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, 'Неверный формат ссылки,попробуйте еще раз!')


def send_weather(message):
    get_weather(message.text)
    weather = get_weather(message.text)
    bot.send_message(message.chat.id, weather)


def send_time(message):
    time_world(message.text)
    get_time = time_world(message.text)
    bot.send_message(message.chat.id, get_time)


def get_input(message):
    if not any(message.text in item for item in languages):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn8 = types.KeyboardButton('English')
        btn9 = types.KeyboardButton('German')
        btn10 = types.KeyboardButton('Polish')
        btn11 = types.KeyboardButton('Spanish')
        btn12 = types.KeyboardButton('French')
        markup.add(btn8, btn9, btn10, btn11, btn12)
        bot.send_message(message.chat.id, 'К сожалению вы не выбрали "язык" для перевда ...', reply_markup=markup)

    else:
        sent = bot.send_message(message.chat.id, "Вы выбрали " + message.text + "\n"
                                                                                "➡️ Введите слово или фразу на русском")
        languages_switcher = {
            'English': send_eng_trans,
            'German': send_ger_trans,
            'Polish': send_pol_trans,
            'Spanish': send_spa_trans,
            'French': send_fra_trans
        }

        lang_response = languages_switcher.get(message.text)
        bot.register_next_step_handler(sent, lang_response)


def send_eng_trans(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=True)  # Return to start keyboard
    bot.send_message(message.chat.id, to_en(message.text), reply_markup=start_markup)


def send_ger_trans(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=False)  # Return to start keyboard

    bot.send_message(message.chat.id, to_de(message.text), reply_markup=start_markup)


def send_pol_trans(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=False)  # Return to start keyboard

    bot.send_message(message.chat.id, to_pl(message.text), reply_markup=start_markup)


def send_spa_trans(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=False)  # Return to start keyboard

    bot.send_message(message.chat.id, to_es(message.text), reply_markup=start_markup)


def send_fra_trans(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=False)  # Return to start keyboard

    bot.send_message(message.chat.id, to_fr(message.text), reply_markup=start_markup)


bot.polling(none_stop=True)
