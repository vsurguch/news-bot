import feedparser

LENTA_FEED = 'http://lenta.ru/rss/news'

class MyTeleBotDB:
    '''
    класс для работы с БД. Пока в качестве заглушки работаен напрямую с rss,
    а не с БД.
    '''
    def get_news(self, key=None):
        feed = feedparser.parse(LENTA_FEED)
        news = feed['entries'][:10]
        return news


if __name__ == '__main__':
    db = MyTeleBotDB()
    db.get_news()
