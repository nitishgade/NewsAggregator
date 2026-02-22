import datetime
import os
import youtube_transcript_api
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_URL = "https://youtube.googleapis.com/youtube/v3/"

requestSession = requests.Session()
requestSession.headers.update({
	"Accept": "application/json"
})
requestSession.params.update({
	"key": YOUTUBE_API_KEY
})

'''
Get the latest videos from either a channel or a username within the past given hours.
If both channel and username are provided, channel takes precedence.
'''
def get_latest_videos(username, hours):
	assert username, "Username must be provided"
	playlistId = get_playlist_from_channel(username) # get playlistId from channel username

	videosInPlaylist = get_videos_from_playlist(playlistId) # now get the videos from that playlist

	latestVideos = []
	now = datetime.datetime.now(datetime.timezone.utc)
	for video in videosInPlaylist:
		publishedAt = video["snippet"]["publishedAt"]
		publishedAtDatetime = datetime.datetime.fromisoformat(publishedAt.replace("Z", "+00:00"))
		dateDiff = now - publishedAtDatetime
		hoursDiff = dateDiff.total_seconds()/3600
		if hoursDiff <= hours:	
			latestVideos.append(video)
	
	return latestVideos

'''
Get the playlistId for the uploads of a channel given the channel's username.
'''
def get_playlist_from_channel(username):
	channelUrl = f"{YOUTUBE_API_URL}channels"
	params = {
		"part": "contentDetails",
		"forUsername": username
	}
	channelResponse = requestSession.get(channelUrl, params=params)
	channelResponse.raise_for_status()
	channelData = channelResponse.json()
	return channelData["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

'''
Get the videos from a playlist given the playlistId.
'''
def get_videos_from_playlist(playlistId):
	assert playlistId, "Playlist ID must be provided"
	playlistItemsUrl = f"{YOUTUBE_API_URL}playlistItems"
	params = {
		"part": "snippet,contentDetails",
		"playlistId": playlistId,
		"maxResults": 50
	}
	videoResponse = requestSession.get(playlistItemsUrl, params=params)
	videoResponse.raise_for_status()
	videoData = videoResponse.json()

	return videoData["items"]

'''
Get the transcript text from a video given the videoId.
'''
def get_transcript_from_video(videoId):
	try:
		transcriptApi = youtube_transcript_api.YouTubeTranscriptApi()
		transcript = transcriptApi.fetch(videoId)
		transcript = transcript.to_raw_data()
		transcriptText = " ".join([item["text"] for item in transcript])
	except youtube_transcript_api.TranscriptsDisabled:
		print(f"INFO: Transcripts are disabled for video {videoId}.")
	except youtube_transcript_api.NoTranscriptFound:
		print(f"INFO: No English/suitable transcript found for video {videoId}.")
	except Exception as e:
		print(f"ERROR: An unexpected error occurred for {videoId}: {e}")

	return transcriptText