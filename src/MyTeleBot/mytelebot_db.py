import feedparser
import time

LENTA_FEED = 'http://lenta.ru/rss/news'

class MyTeleBotDB:
    '''
    класс для работы с БД. Пока в качестве заглушки работаен напрямую с rss,
    а не с БД.
    '''
    def get_news(self, key=None):
        feed = feedparser.parse(LENTA_FEED)
        news = feed['entries'][:10]
        for n in news:
            n['published'] = self.format_time(n.get('published'))
        return news

    def format_time(self, time_str):
        return time_str[17:25]


if __name__ == '__main__':
    db = MyTeleBotDB()
    db.get_news()
