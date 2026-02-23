import os
import json
import datetime
import sys
import feedparser
from curl_cffi import requests
import trafilatura
from helpers import get_article_content

OPENAI_NEWS_RSS="https://openai.com/news/rss.xml"

'''
Get the latest news from OpenAI's news RSS feed within the past given hours.
'''
def get_latest_openai_news(hours):
	feed = feedparser.parse(OPENAI_NEWS_RSS)
	latest_news = []
	now = datetime.datetime.now(datetime.timezone.utc)
	for entry in feed.entries:
		publishedAt = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
		dateDiff = now - publishedAt
		hoursDiff = dateDiff.total_seconds()/3600
		if hoursDiff <= hours:
			latest_news.append({
				"title": entry.title,
				"link": entry.link,
				"summary": entry.summary if 'summary' in entry else "",
				"text": get_article_content(entry.link)[1],
				"published_at": publishedAt
			})