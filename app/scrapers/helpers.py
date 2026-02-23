from curl_cffi import requests
import trafilatura
from trafilatura.settings import use_config

'''
Fetch the content of an article given its URL. Uses curl_cffi to get the webpage and trafilatura to extract the main content.
'''
def get_article_content(url):
	try:
		new_config = use_config()
		new_config.set("DEFAULT", "MAX_REDIRECTS", "5")
		response = requests.get(url, impersonate="chrome120")
		if response.status_code == 200:
			metadata = trafilatura.metadata.extract_metadata(response.text)
			content = trafilatura.extract(response.text, config=new_config)
			return (metadata.title,content) if content else "No content extracted."
		else:
			return f"Failed with status: {response.status_code}"
	except Exception as e:
		return f"Could not fetch content for {url}: \nError is {e}"