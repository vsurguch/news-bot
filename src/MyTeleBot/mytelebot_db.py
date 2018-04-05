import pymongo


DEBUG = False

class MyTeleBotDB:
    '''
    класс для работы с БД.
    '''
    def __init__(self):
        self.client = pymongo.MongoClient(serverSelectionTimeoutMS=2000)
        try:
            self.client.admin.command('ismaster')
        except pymongo.errors.ServerSelectionTimeoutError:
            raise

        self.db = self.client.telebot
        self.required = {'title', 'published', 'link', 'summary', 'base'}
        
    def get_news(self, key='', count=10) -> []:
        '''
        Принимает на вход:
        key   - (пока не используется)
        count - количество возвращаемых новостей

        Возвращает список из словарей, каждый словарь - отдельная новость.
        Словарь имеет следующие поля:
        {
            'title':     -заголовок новости,
            'published': -таймстамп времени публикации - тип float,
            'link':      -адрес новости,
            'summary':   -краткое изложение новости,
            'base':      -адрес rss-канала
        }
        '''
        news = self.db.news.find() \
                   .sort('published', pymongo.DESCENDING) \
                   .limit(count)
        return news

    def set_news(self, news: dict):
        '''
        Принимает обязательный параметр news типа dict.
        Обязательные поля в словаре:
        {
            'title':     -заголовок новости,
            'published': -таймстамп времени публикации - тип float,
            'link':      -адрес новости,
            'summary':   -краткое изложение новости,
            'base':      -адрес rss-канала
        }
        Также можно добавлять другие поля с дополнительной информацией.
        '''
        if not isinstance(news, dict):
            error = 'expected dict instance, {} found'.format(type(news))
            raise TypeError(error)

        if not self.required <= set(news):
            error = 'not found required key(s) {}' \
                .format(self.required - set(news))
            raise TypeError(error)

        if not isinstance(news['published'], float):
            error = "a float is required for 'published' (got type {})" \
                .format(type(news['published']))
            raise TypeError(error)

        self.db.news.insert_one(news)

    def get_last_published(self, base):
        '''
        Возвращает время публикации последней новости для данного rss-канала.
        Если в БД для канала еще нет новостей, возвращает 0.0
        base - адрес rss-канала.
        '''
        try:
            last_news = self.db.news.find({'base': base}, {'published': 1}) \
                            .sort('published', pymongo.DESCENDING) \
                            .limit(1) \
                            .next()
        except StopIteration:
            return 0.0
        last_time = last_news['published']
        return last_time
        

if __name__ == '__main__':
    # Примитивное тестирование
    # Надо определиться с библиотекой для тестов
    if DEBUG:
        db = MyTeleBotDB()
        db.db.news.drop()
        db.set_news(
            {
                'title': 'First news',
                'published': 1234.55,
                'link': 'https://bla.bla/novost_dnja',
                'summary': 'lorem ipsum',
                'base': 'https://bla.bla/rss',
            }
        )
        try:
            db.set_news(
                {
                    'title': 'First news',
                    'published': 1234.55,
                    'summary': 'lorem ipsum',
                    'base': 'https://bla.bla/rss',
                }
            )
        except TypeError as err:
            print(err)
        print(list(db.get_news()))
        print(db.get_last_published('http://xyz.net')) # вернет 0.0
        print(db.get_last_published('https://bla.bla/rss')) 
