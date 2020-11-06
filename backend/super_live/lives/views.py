from django.shortcuts import render

# Create your views here.
from apiclient.discovery import build

DEVELOPER_KEY = "AIzaSyBvde10k7ikU_qQU5CajasqJ57AcmlTTJc" #下川穣汰のYoutube API Key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY,cache_discovery=False)
response = youtube.videos().list(part="snippet,liveStreamingDetails",id="SORD03t7nlo").execute()　#idの部分はhttps://www.youtube.com/watch?v='hogehoge' <-ここ！
#print(response) 辞書型で動画のsnippetとliveStreamingDetailの情報が見れる
print(response["items"][0]["liveStreamingDetails"]["concurrentViewers"])
