import telebot
from extensions import UserException, Convertor
from config import TOKEN, cur

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message) #стартовая команда боту
    bot.send_message(
        message.chat.id,
        '''Отправьте сообщение боту в виде <имя валюты, цену которой хотите узнать> \
<имя валюты, в которой нужно узнать цену> <количество валюты> укажите  три слова через пробел.
Доступные валюты можно посмотреть командой /values'''
    )


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:\n'
    for i in cur.keys():
        text += i + '\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    res_message = message.text.lower().split()

    try:
        if len(res_message) != 3:
            raise UserException('Неверное количество параметров!')
        base, quote, amount = res_message
        if amount.find(','):
            amount = amount.replace(',', '.')
        answer = Convertor.get_price(base, quote, amount)
    except UserException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)
