import feedparser
import time

LENTA_FEED = 'http://lenta.ru/rss/news'

class MyTeleBotDB:
    '''
    класс для работы с БД. Пока в качестве заглушки работаен напрямую с rss,
    а не с БД.
    '''
    def get_news(self, key='') -> []:
        '''
        Возвращает список из словарей, каждый словарь - отдельная новость.
        Словарь имеет следующие поля:
        {
            'title':     -заголовок новости,
            'published': -таймстамп времени публикации,
            'link':      -адрес новости,
            'summary':   -краткое изложение новости,
            'base':      -адрес rss-канала
        }
        Принимает на вход необязательный параметр key (пока не используется)
        '''
        feed = feedparser.parse(LENTA_FEED)
        news = feed['entries'][:10]
        for n in news:
            n['published'] = self.format_time(n.get('published'))
        return news

    def set_news(self, news: dict):
        '''
        Принимает обязательный параметр news типа dict.
        Обязательные поля в словаре:
        {
            'title':     -заголовок новости,
            'published': -таймстамп времени публикации,
            'link':      -адрес новости,
            'summary':   -краткое изложение новости,
            'base':      -адрес rss-канала
        }
        '''
        pass

    


if __name__ == '__main__':
    db = MyTeleBotDB()
    db.get_news()
