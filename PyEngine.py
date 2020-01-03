from mysql.connector import MySQLConnection, Error
from requests import get
from bs4 import BeautifulSoup, SoupStrainer
import random

class Crawler:

    host = 'localhost'
    database = 'db_google'
    user = 'root'
    password = 'root'

    def __init__(self, host=None,database=None,user=None,password=None):
        if host:
            self.host = host
        if database:
            self.database = database
        if user:
            self.user = user
        if password:
            self.password = password
    
    
    def Crawl(self, url):

        with get(url) as response:
            content = BeautifulSoup(response.text, "lxml")

            for link in content.find_all("a"):
                try:
                    if link.attrs["href"].startswith('/'):
                        yield url+link.attrs["href"]+'\n'
                    elif link.attrs["href"].startswith('javascript:void(0)'):
                        pass
                    else:
                        yield link.attrs["href"]+'\n'
                except KeyError:
                    pass

if __name__ == '__main__':
    bot = Crawler()
    url = bot.Crawl(url='http://google.com')
    print(next(url))
