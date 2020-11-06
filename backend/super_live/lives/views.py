import json
import urllib.parse

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Live, Reactions
from django.utils import timezone
from apiclient.discovery import build


def SearchYtId(request):
    if 'name' in request.GET:
        name = request.GET['name']
        name = urllib.parse.unquote(name)
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
    DEVELOPER_KEY = "AIzaSyBnUnVdQgp1W4AFuZ_-ElSTAt79M0aE0y0" #Youtube API Keyを入れるところ
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

        liveName = urllib.parse.unquote(liveName)
        liveUser = urllib.parse.unquote(liveUser)
        pub_date = timezone.now()

        l.liveId = liveId
        l.liveUser = liveUser
        l.pub_date = pub_date
        l.liveName = liveName
        l.save()

        l.reactions_set.create(reaction='happy', reactionCount=0)

        message = 'success'
    
    else:
        message='fauler'

    params={
        'message':message,
    }

    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)


def setReaction(request):
    if 'id' in request.GET and 'reaction' in request.GET:
        id = request.GET['id']
        re = request.GET['reaction']
        if id in Live.objects.values_list('liveId', flat=True) and re == 'happy':
            l = get_object_or_404(Live, liveId = id)
            try:
                selected_reaction = l.reactions_set.get(reaction=re)
            except (KeyError, Reactions.DoNotExist):
                message = 'failure'
                params = {
                    'message':message,
                }
                json_str = json.dumps(params, ensure_ascii=False, indent=2)
                return HttpResponse(json_str)
            else:
                selected_reaction.reactionCount += 1
                selected_reaction.save()

                message = 'success'
                params = {
                    message:'success',
                }
                json_str = json.dumps(params, ensure_ascii=False, indent=2)
                return HttpResponse(json_str)
        else:
            message = 'failure'
            params = {
                'message':message,
            }
            json_str = json.dumps(params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str)
    else:
        message = 'failure'
        params = {
            'message':message,
        }
        json_str = json.dumps(params, ensure_ascii=False, indent=2)
        return HttpResponse(json_str)
