from newspaper import Article
import feedparser
import json
import sqlite3
from time import sleep
from rm_old_news import rm_news

NEWS_URLS_PATH = './data/urls.json'
DB_PATH = './data/news.sqlite3'
CATEGORIES_ORDER_PATH = './data/categories_order.json'

ARTICLE_CODES = {'english': 'en', 'hindi': 'hi'}

class ParseNews():
	def __init__(self):
		self.urls = json.load(open(NEWS_URLS_PATH))
		self.sort_order = json.load(open(CATEGORIES_ORDER_PATH))
		self.feeds = dict()

	def get_news(self, language):
		urls_type = self.urls[language]
		topics = list(urls_type.keys())

		for topic in topics:
			for news_url in urls_type[topic]:
				article_no = 20
				print(news_url)
				news_feed = feedparser.parse(news_url)
				for news in news_feed.entries:
					try:
						title, url, date = news['title'], news['link'], news['published']
						article = Article(url, language=ARTICLE_CODES[language])
						article.download()
						article.parse()
						summary = article.text

						self.feeds[title] = dict()
						self.feeds[title]['url'] = url
						self.feeds[title]['date'] = date
						self.feeds[title]['summary'] = summary
						self.feeds[title]['category'] = topic
						print("DONE: {}, {}".format(news['title'], topic))
					except:
						print("FAILED: {}".format(news['title']))

					if article_no == 0:
						break
					else:
						article_no -= 1

	def store_news(self, language):
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		c.execute("""CREATE TABLE IF NOT EXISTS News
						(title text, 
						 link text, 
						 published text, 
						 summary text,
						 category text,
						 language text)""")

		for title in self.feeds:
			c.execute("""INSERT INTO News (title, 
											link, 
											published, 
											summary, 
											category, 
											language) VALUES (?, ?, ?, ?, ?, ?)""",
						(title, 
						self.feeds[title]['url'], 
						self.feeds[title]['date'], 
						self.feeds[title]['summary'], 
						self.feeds[title]['category'], 
						language))
		conn.commit()
		conn.close()

	def fetch_news(self, language):
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		news_list = c.execute("""SELECT title, link, published, summary, category FROM News WHERE language=?""", (language, )).fetchall()
		news_json = dict()

		for news in news_list:
			news_json[news[0]] = dict()
			news_json[news[0]]['url'] = news[1]
			news_json[news[0]]['published'] = news[2]
			news_json[news[0]]['summary'] = news[3]
			news_json[news[0]]['category'] = news[4]

		conn.close()
		return news_json

	def fetch_categories(self, language):
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		categories = set(c.execute("""SELECT category FROM News WHERE language=?""", (language, )).fetchall())

		conn.close()
		categories = sorted([category[0] for category in categories], 
		                     key=lambda x: self.sort_order.index(x))
		return categories

if __name__ == '__main__':
	langs = ['hindi', 'english']

	for language in langs:
		parse = ParseNews()
		parse.get_news(language)
		parse.store_news(language)
