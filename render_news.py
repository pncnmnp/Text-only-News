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
	exception = str()
	try:
		site_name = urlparse(news[title]['url']).hostname.replace('feeds.', '')
		return render_template('summary.html', 
							title=title, 
							summary=news[title]['summary'].split('\n'),
							link=news[title]['url'],
							published=news[title]['published'],
							site_name=site_name)
	except:
		exception = 'The summary for the following title does not exist!'
		return render_template('error.html',
								exception=exception)

@app.errorhandler(404)
def page_not_found(error):
	exception = 'Error 404: The page does not exist!'
	return render_template('error.html', exception=exception), 404

@app.errorhandler(500)
def internal_server(error):
	exception = 'Error 500: There is a problem with our server. Please try again!'
	return render_template('error.html', exception=exception), 500
