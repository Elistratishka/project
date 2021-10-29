import os
import  telebot
from dotenv import load_dotenv
from extensions import get_data, convert

load_dotenv()
token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    rules = "Бот применим для конвертации стоимости инстранных валют и рубля по курсу ЦБ на сегодня, "\
            "а также для конвертации стоимости токенов с площадки alcor exchange\n"\
            "Для использования бота напишите ему сообщение в формате:\n <количество валюты>" \
            " <валюта из которой переводить> <валюта в которую переводить>\n" \
            "Введите команду /values для получения информации о доступных для конвертации валютах и токенах"
    bot.reply_to(message, rules)

@bot.message_handler(commands=['values'])
def start(message: telebot.types.Message):
    text = 'Доступные валюты: '
    data = get_data()
    for values in data.keys():
        text = '\n'.join((text, values, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def work(message: telebot.types.Message):
    data = get_data()
    try:
        letter = message.text.replace(',', '.').upper().split(' ')
        if len(letter) != 3:
            raise ConvertionException("Введено неверное количество параметров.")
        amount, quote, base = letter
        cost = convert(amount, quote, base)
    except Exception:
        bot.send_message('Извините, что-то пошло не так')
    text = f'Стоимость {amount} {quote} в {base} = {cost}'
    bot.send_message(message.chat.id, text)


bot.polling()















