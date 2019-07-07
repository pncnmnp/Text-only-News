import sqlite3

def rm_news(DB_PATH):
	'''
    Parameters : 'DB_PATH' = 'string' type containing the path of
                              SQlite DB to be filtered.
    
    Returns: Does not return anything, 
    
    Filters the entire News database to accommodate latest news.
	'''
	try:
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		news_list = c.execute("""SELECT title, link, published, summary FROM News""").fetchall()

		for news in news_list:
			c.execute("DELETE FROM News WHERE title=?", (news[0],))

		conn.commit()
		conn.close()
	except:
		print("DB NOT CLEARED!")
		pass

if __name__ == "__main__":
	from get_news import DB_PATH
	rm_news(DB_PATH)
