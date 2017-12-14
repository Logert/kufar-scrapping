import config
import telebot
import scrapping


bot = telebot.TeleBot(config.token)
text = scrapping.getNews()
index = 0


def adsToMessage(ind):
    return 'Цена: ' + str(text[ind].get('price')) + '\n' + \
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
    bot.send_message(message.chat.id, adsToMessage(index))
    index += 1


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


# file = open('page.json', 'w')
# file.write(json.dumps(getNews()))
# file.close()


if __name__ == '__main__':
    bot.polling(none_stop=True)
