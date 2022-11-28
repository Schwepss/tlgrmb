import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу с ботом, введите комманду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переведимой валюты> \n \n Чтобы увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Задан не верный параметр!")

        what, into, amount = values
        total_amount = CryptoConverter.convert(what, into, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена {amount} {what} в {into} - {total_amount}"
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)