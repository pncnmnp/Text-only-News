from newspaper import Article
import feedparser
import json
import sqlite3

NEWS_URLS_PATH = './data/urls.json'
DB_PATH = './data/news.sqlite3'

class ParseNews():
	def __init__(self):
		self.urls = json.load(open(NEWS_URLS_PATH))
		self.feeds = dict()

	def get_news(self):
		for news_url in self.urls:
			news_feed = feedparser.parse(news_url)
			for news in news_feed.entries:
				try:
					title, url, date = news['title'], news['link'], news['published']
					article = Article(url)
					article.download()
					article.parse()
					summary = article.text

					self.feeds[title] = dict()
					self.feeds[title]['url'] = url
					self.feeds[title]['date'] = date
					self.feeds[title]['summary'] = summary
				except:
					print("FAILED: {}".format(news['title']))

	def store_news(self):
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		c.execute("""CREATE TABLE IF NOT EXISTS News
						(title text, 
						 link text, 
						 published text, 
						 summary text)""")

		for title in self.feeds:
			c.execute("""INSERT INTO News (title, link, published, summary) VALUES (?, ?, ?, ?)""",
					(title, self.feeds[title]['url'], self.feeds[title]['date'], self.feeds[title]['summary']))

		conn.commit()
		conn.close()

	def fetch_news(self):
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		news_list = c.execute("""SELECT title, link, published, summary FROM News""").fetchall()
		news_json = dict()

		for news in news_list:
			news_json[news[0]] = dict()
			news_json[news[0]]['url'] = news[1]
			news_json[news[0]]['published'] = news[2]
			news_json[news[0]]['summary'] = news[3]

		conn.close()
		return news_json