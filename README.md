<p align="center">
<img src="https://github.com/pncnmnp/Text-only-News/blob/master/screenshots/news-headlines.png">
</p>
<p>
<img alt="Online" src="https://img.shields.io/website/https/textnews.pythonanywhere.com.svg?down_color=red&down_message=offline&up_color=green&up_message=online"> <img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"> <img alt="flask version" src="https://img.shields.io/badge/flask%20version-1.0.3-blue.svg">
</p>

### Description
Text-only news is a website/progressive-web-app to provide clutter-free news in various languages. This is a non-commercial attempt to provide news in places with slow-internet connectivity especially in rural areas. With low request sizes and fast loading time, the site is perfect for low bandwidth connections.<br/>
Features of this site are:
* Low request sizes, fast loading time
* Search articles with relevant keyword
* Can be used as a Progressive Web App (PWA)
* News are segregated into various categories
* Multilingual, currently supporting - English, Hindi
* Clean UI

The site is currently hosted on [PythonAnywhere](https://pythonanywhere.com): [Text-Only News](https://textnews.pythonanywhere.com)

### How to run (Locally)
Enter the urls you want to scrape in `./data/urls.json` with appropriate `language` and `categories`. The format for the same is:
`{
	'language_1': {'category_1': ['link_1', 'link_2', ...],
                   'category_2': ['link_1', 'link_2', ...]},
    'language_2': {...}
 }`

If you add any categories in `./data/urls.json`, make sure to list them in `./data/categories_order.json`

To fetch the news and store them locally in `./data/news.sqlite3`, run:
`python get_news.py language`
where `language` is a string, whose value should be from `language_1, language_2, ...` (from `./data/urls.json`)

By default, values are appended at the end of the database. To truncate the DB, run `rm_old_news.py`.

### License
This project is under MIT License. The news content is a copyright property of the respective news platform. Currently news is rendered from RSS feeds provided by [Reuters](https://in.reuters.com/tools/rss), [NDTV](https://www.ndtv.com/rss) and [Dainik Bhaskar](https://www.bhaskar.com/). The site logo is under [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/) by [Designmodo](https://www.flaticon.com/authors/designmodo).
