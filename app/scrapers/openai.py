import os
import json
import datetime
import sys
import feedparser
from curl_cffi import requests
import trafilatura

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
				"text": get_article_content(entry.link),
				"published_at": publishedAt
			})


'''
Fetch the content of an article given its URL. Uses curl_cffi to get the webpage and trafilatura to extract the main content.
'''
def get_article_content(url):
	try:
		response = requests.get(url, impersonate="chrome120")
		if response.status_code == 200:
			content = trafilatura.extract(response.text)
			return content if content else "No content extracted."
		else:
			return f"Failed with status: {response.status_code}"
	except Exception as e:
		return f"Could not fetch content for {url}: \nError is {e}"