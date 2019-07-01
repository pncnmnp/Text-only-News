import sqlite3
from get_news import DB_PATH

def rm_news():
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	news_list = c.execute("""SELECT title, link, published, summary FROM News""").fetchall()

	for news in news_list:
		c.execute("DELETE FROM News WHERE title=?", (news[0],))

	conn.commit()
	conn.close()

if __name__ == "__main__":
	rm_news()
