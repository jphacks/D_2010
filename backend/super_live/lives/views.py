import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Live
from django.utils import timezone
from apiclient.discovery import build

def SearchYtId(request):
    if 'name' in request.GET:
        name = request.GET['name']
        if name in Live.objects.values_list("liveName", flat=True):
            liveId = ', '.join([q.liveId for q in Live.objects.filter(liveName=name)])
            pub_data = timezone.now()
            message = 'success'
        else:
            liveId='NA'
            pub_data = 'NA'
            message = 'do not exist such a live'
    
    else:
        name='NA'
        liveId='NA'
        pub_data='NA'
        message='send live name'
    
    params={
        'liveName':name,
        'liveId':liveId,
        'message':message,
    }

    
    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)



def addVideos(request):
    DEVELOPER_KEY = "" #Youtube API Keyを入れるところ
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    if 'id' in request.GET and 'user' in request.GET:
        l = Live()
        liveUser = request.GET['user']
        liveId = request.GET['id']
        

        #liveNameにliveId(YouTubeIDと同じ)からとってきたライブのタイトルをとってきてほしい
        youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY,cache_discovery=False)
        response = youtube.videos().list(part="snippet,liveStreamingDetails",id=liveId).execute()
        liveName = response["items"][0]["snippet"]["title"]

        pub_date = timezone.now()

        l.liveId = liveId
        l.liveUser = liveUser
        l.pub_date = pub_date
        l.liveName = liveName

    
    else:
        user = 'NA'
        liveId = 'NA'
        pub_data = 'NA'
        message = 'Failure to add video'

    params = {
        'user': user,
        'liveId':liveId,
        'message':message,
    }

    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)


     
