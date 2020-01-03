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

    def extract_info(self, url):
        ATTRIBUTES = ['description', 'keywords', 'Description', 'Keywords'] #Using this array list an a filter for collecting the meta data

        entry = {'url': url}

        try:
            r = requests.get(url)
        except Exception as e:
            print('Could not load page {}. Reason: {}'.format(url, str(e)))
            continue

        if r.status_code == 200:

            soup = BeautifulSoup(r.content, 'html.parser')
            entry['title'] = soup.title.string
            meta_list = soup.find_all("meta")

            for meta in meta_list:
                if 'name' in meta.attrs:
                    name = meta.attrs['name']
                    if name in ATTRIBUTES:
                        entry[name.lower()] = meta.attrs['content']

            if len(entry) == 3:
                yield entry

            else:
                yield {'url':0,'description':0,'keywords':0}
                print('Could not find all required attributes for URL {}'.format(url))

        else:
            yield {'url':False,'description':False,'keywords':False}
            print('Could not load page {}.Reason: {}'.format(url, r.status_code))

    #inserts data into the database
    def insert_site(self, id='NULL', url, title, description, keywords, clicks, scrapped=0):
        query = "INSERT INTO sites(id,url,title,description,keywords,clicks,scrapped) " \
                "VALUES(%s,%s,$s,$s,$s,$s)"
        args = (id, url, title, description, keywords, clicks,scrapped)

        try:
            """
            by connect to the database each time we call the function
            it cancels the timeout from mysql server
            """
            conn = connect(host='localhost',
                            database='db_google',
                            user='root',
                            password='root')

            cursor = conn.cursor()
            cursor.execute(query, args)

            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')

            conn.commit()

if __name__ == '__main__':
    bot = Crawler()
    url = bot.Crawl(url='http://google.com')
    print(next(url))
