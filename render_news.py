from flask import Flask, render_template, request, redirect
import get_news
from urllib.parse import urlparse

DEFAULT = 'english'
LANG_SUPPORTED = [DEFAULT, 'hindi']

app = Flask(__name__)
parsed = get_news.ParseNews()

def get_titles(language, search_query):
	news = parsed.fetch_news(language)
	# Searching query in titles
	titles = [title for title in list(news.keys()) 
	                    if title.lower().find(search_query.lower()) >= 0]

	# searching query in summaries of each titles
	titles += [title for title in list(news.keys()) 
	                    if news[title]['summary'].lower().find(search_query.lower()) >= 0]
	return list(set(titles))

@app.route('/', methods=['GET'])
def index():
	return redirect("/english")

@app.route('/<lang>', methods=['GET'])
def display_headlines(lang):
	if lang in LANG_SUPPORTED:
		news = parsed.fetch_news(lang)
		try:
			titles = get_titles(lang, request.args['search'])
		except:
			titles = list(news.keys())
		return render_template('headlines.html', titles=titles, lang=lang)

@app.route('/<lang>/<category>')
def display_category(lang, category):
	if lang in LANG_SUPPORTED:
		news = parsed.fetch_news(lang)
		titles = list()
		for article in news:
			if news[article]['category'] == category:
				titles.append(article)
		return render_template('headlines.html', titles=titles, lang=lang)	

@app.route('/summary', methods=['GET'])
def display_summary():
	title = request.args['title']
	lang = request.args['language']
	news = parsed.fetch_news(lang)
	exception = str()
	try:
		site_name = urlparse(news[title]['url']).hostname.replace('feeds.', '')
		return render_template('summary.html', 
							title=title, 
							summary=news[title]['summary'].split('\n'),
							link=news[title]['url'],
							published=news[title]['published'],
							site_name=site_name,
							lang=lang)
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
