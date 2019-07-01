from flask import Flask, render_template, request
import get_news
from urllib.parse import urlparse

app = Flask(__name__)
parsed = get_news.ParseNews()

@app.route('/')
def display_headlines():
	news = parsed.fetch_news()
	titles = list(news.keys())

	return render_template('headlines.html', titles=titles)

@app.route('/summary', methods=['GET'])
def display_summary():
	title = request.args['title']
	news = parsed.fetch_news()
	site_name = urlparse(news[title]['url']).hostname.replace('feeds.', '')
	return render_template('summary.html', 
							title=title, 
							summary=news[title]['summary'].split('\n'),
							link=news[title]['url'],
							published=news[title]['published'],
							site_name=site_name)