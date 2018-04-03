import telebot
from mytoken import TOKEN


class MyTeleBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.init_handlers()

    def init_handlers(self):
        ''' Инициализация обработчиков событий telegram '''
        @self.bot.message_handler(commands=['start', 'help'])
        def command_help(message):
            self.bot.send_message(message.chat.id, 'Нужна помощь?')

        @self.bot.message_handler(content_types=['text'])
        def handle_message(message):
            self.bot.send_message(message.chat.id, 'Ответка')

    
    def run(self):
        self.bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    bot = MyTeleBot()
    bot.run()
