import datetime
from curl_cffi import requests
import xml.etree.ElementTree as ET
import trafilatura
from helpers import get_article_content

ANTHROPIC_SITEMAP_URL="https://www.anthropic.com/sitemap.xml"

'''
Get the latest news from Anthropic research within the past given hours.
'''
def get_latest_anthropic_research(hours):
	response = requests.get(ANTHROPIC_SITEMAP_URL, impersonate="chrome120")
	if response.status_code != 200:
		print(f"Error fetching sitemap: {response.status_code}")
		return []
	
	root = ET.fromstring(response.text)
	namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
	latest_research = []
	now = datetime.datetime.now(datetime.timezone.utc)
	for url in root.findall("ns:url", namespace):
		loc = url.find("ns:loc", namespace).text
		lastmod = url.find("ns:lastmod", namespace).text
		lastmod_datetime = datetime.datetime.fromisoformat(lastmod.replace("Z", "+00:00"))
		dateDiff = now - lastmod_datetime
		hoursDiff = dateDiff.total_seconds()/3600
		if hoursDiff <= hours and "/research/" in loc:
			url_content = get_article_content(loc)
			latest_research.append({
				"link": loc,
				"published_at": lastmod_datetime,
				"text": url_content[1],
				"title": url_content[0]
			})

	return latest_research