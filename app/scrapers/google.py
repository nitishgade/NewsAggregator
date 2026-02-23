import feedparser
import datetime
from helpers import get_article_content

GOOGLE_BLOG_RSS = "https://blog.google/technology/ai/rss/"

'''
Get the latest news from Google Research's news RSS feed within the past given hours.
'''
def get_latest_google_news(hours):
	latest_news = []
	now = datetime.datetime.now(datetime.timezone.utc)
	feed = feedparser.parse(GOOGLE_BLOG_RSS)
	for entry in feed.entries:
		published_at = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
		date_diff = now - published_at
		hours_diff = date_diff.total_seconds() / 3600
		if hours_diff <= hours:
			latest_news.append({
				"title": entry.title,
				"link": entry.link,
				"published_at": published_at,
				"text": get_article_content(entry.link)[1]
			})

	return latest_news