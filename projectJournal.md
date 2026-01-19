# Journal of Project Progress

This journal is here to show how the project progressed over its various stages.

## Step 0: 2026-01-17
#### Step 1: Asking Copilot Agent on the project folder structure
This step includes firstly asking Copilot Agent on how to structure this folder to represent a true project. The prompt I used is below:

* "i want to create an ai technology news aggregator, where i take multiple sources, for example youtube channels, blog posts from openai, google, anthropic, news reports especially from tech news sources (not mainstream media). And I want to scrape those, put them into a database where we have some kind of structure where we have sources, articles, and I want to run a daily digest where we will take all of those articles, and we will give an llm summary around that and based on the user insights that we specify in an agent system prompt, we can generate a daily digest which is going to be short snippets with a link to the original source. from the youtube channels, i want to create a list of channels and then we want to get the latest videos from those channels, we may be able to use the youtube rss feed for that, and for blog posts we can use URLs. i want everything built in a python backend, i want to use a postgresql databse, i want to use sqlalchemy to define the database models and tables, i want the project structure to be an app folder where the app logic is in, and I want a docker folder where we create a minimal setup for the postgresql database, and then later down the line we want to make sure we can easily deploy the whole app to render, and then schedule it every 24 hours to run reports, get everything, and then when we've created the daily digests i want to send an email to my personal inbox with this."

This prompt was intended to be specific and is an approximate paraphrasing of what Dave Ebbelaar asked his AI to figure out the structure of the application, and how he envisions the application working. This prompt includes:
* what the project is, a news aggregator about AI topics
* sources of news, youtube, openai, google, tech news sources
* scrape those sources and put that information in a database
* daily take new articles to provide llm summaries and snippets from sources that would match a user's preferences
* the application is built in a python backend
* the database for the application is postgresql
* sqlalchemy in python to interact with the database
* docker folder to create a postgresql container
* easily deploy the app
* schedule it to get new news every 24 hours
* send an email with the new news to my email

#### Step 2: Specifying more details to Copilot Agent
The second prompt included specifying more details about the project, the prompt was:
* "i also want to use openAI as the LLM provider, for emails i want the easiest possible way to send emails ideally a free service, blog scraping should be full, for agent system prompt we will create a separate folder where all of that with live, and the docker setup should include postgresql"

Here, this includes:
* Use OpenAI for the LLM that will summarize all the news content
* For emails make it easy to send and also be free
* Scrape all of the text in a blog post
* Agent prompts will be in a separate folder
* Docker setup should be for a postgresql container

#### Step 3: Implemented the project structure in my local directory within VSCode
Made the project structure as seen in the repository

#### Step 4: Installed needed packages
Installed the following packages:
* sqlalchemy 
* psycopg2-binary (postgres adapter) 
* requests 
* feedparser (download and parse syndicated feeds https://feedparser.readthedocs.io/en/latest/introduction/) 
* beautifulsoup4
* python-dotenv (take environment variables from a .env file and set them in any environment)
* openai
* ipykernel --dev (ipython kernel for interactive python usage)

using the "uv add" command, which adds dependencies to the project and requirements, more info can be found here: https://docs.astral.sh/uv/reference/cli/#uv-add

#### Step 5: youtube.py script
Started on the youtube.py script to understand what packages to install, and how to get transcript data from YouTube for its videos.

## Step 1: 2026-01-18
This step mainly included figuring out how to traverse the YouTube Data API v3 to get YouTube videos

#### Step 1: Find YouTube API to get videos
Followed the instructions linked here, https://developers.google.com/youtube/v3/quickstart/python#step_1_set_up_your_project_and_credentials, to set up an API_KEY and use the YouTube API.

#### Step 2: Get YouTube videos based on a channel username
Went to YouTube's API documentation here, https://developers.google.com/youtube/v3/docs, to find the API methods available under "Channels" (https://developers.google.com/youtube/v3/docs/channels).

Saw that there's a list channels API available (https://developers.google.com/youtube/v3/docs/channels/list) that lists all of the channel resources available in a particular channel, tried it out as a curl command such as:

```
curl 'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={{channelUsername}}&key={{API_KEY}}' --header 'Accept: application/json' --compressed
```

This response then gives the playlist ID that YouTube uses an object for all the videos of a channel, so then I read the documentation on how to get the videos from a playlist ID, and got this API (https://developers.google.com/youtube/v3/docs/playlistItems/list) that can list all the videos in a specified playlist, tried it out as a curl command such as:

```
curl 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=10&playlistId={{playlistId}}&key={{YOUR_API_KEY}}' --header 'Accept: application/json' --compressed
```

Then got the JSON response that lists out the videos, and coded all of this up in the youtube.py file.