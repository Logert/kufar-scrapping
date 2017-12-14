import config
import telebot
import scrapping
import json


bot = telebot.TeleBot(config.token)
text = scrapping.getNews()
index = 0


def adsToMessage(ind):
    return '№ ' + str(index) + '\n' + \
           'Цена: ' + str(text[ind].get('price')) + '\n' + \
           'Название: ' + str(text[ind].get('title')) + '\n' + \
           'Ссылка ' + str(text[ind].get('link'))


@bot.message_handler(commands=["start"])
def handleStart(message):
    bot.send_message(message.chat.id, 'Привет ' + message.chat.first_name + ' ' + message.chat.last_name)


@bot.message_handler(commands=["ads"])
def handleStart(message):
    bot.send_message(message.chat.id, 'найдено ' + str(len(text)) + ' объявлений на kufar.by.')


@bot.message_handler(commands=["first"])
def handleStart(message):
    bot.send_message(message.chat.id, adsToMessage(0))


@bot.message_handler(commands=["next"])
def handleStart(message):
    global index
    number = message.text[6:]
    if (message.text[:5] == '/next' and number.isdigit()):
        for mess in range(index, index + int(number)):
            if (index != (len(text)-1)):
                bot.send_message(message.chat.id, adsToMessage(mess))
                index += 1
            else:
                bot.send_message(message.chat.id, 'Объявлений больше нет.')
                break
    else:
        bot.send_message(message.chat.id, adsToMessage(index))
        if (index == (len(text)-1)):
            bot.send_message(message.chat.id, 'Объявлений больше нет.')
        else:
            index += 1


@bot.message_handler(commands=["prev"])
def handleStart(message):
    global index
    if (index != 0):
        bot.send_message(message.chat.id, adsToMessage(index))
        index -= 1
    else:
        bot.send_message(message.chat.id, 'Первое объявление')


@bot.message_handler(commands=["lowprice"])
def handleStart(message):
    global text, index
    index = 0
    text = sorted(text, key=lambda ads: ads.get('price'))
    file = open('page.json', 'w')
    file.write(json.dumps(text))
    file.close()
    bot.send_message(message.chat.id, 'Объявления отсортированы от дешевых к дорогим.')


@bot.message_handler(commands=["price"])
def handleStart(message):
    global text, index
    index = 0
    number = message.text[7:]
    if (message.text[:6] == '/price' and number.isdigit()):
        text = list(filter(lambda ads: ads.get('price') > int(number), text))
        bot.send_message(message.chat.id, 'Объявления с ценой от ' + number)


@bot.message_handler(commands=["new"])
def handleStart(message):
    global text, index
    text = scrapping.getNews()
    index = 0
    bot.send_message(message.chat.id, 'Загружены новые объявления, ' + str(len(text)))


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)


# file = open('page.json', 'w')
# file.write(json.dumps(text))
# file.close()


if __name__ == '__main__':
    bot.polling(none_stop=True)
