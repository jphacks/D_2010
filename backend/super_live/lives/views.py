import json
import urllib.parse

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Live, Reactions
from django.utils import timezone
from apiclient.discovery import build


reactionSet = ['happy', 'sad', 'wow']

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
    DEVELOPER_KEY = "You're API Key" #Youtube API Keyを入れるところ
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

        for re in reactionSet:
            l.reactions_set.create(reaction=re, reactionCount=0)

        message = 'success'
    
    else:
        message='fauler'

    params={
        'message':message,
    }

    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)


def setReaction(request):
    if 'id' in request.GET:
        id = request.GET['id']
        re = request.GET['reaction']
        if id in Live.objects.values_list('liveId', flat=True) and re in reactionSet:
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
                    'message':'success',
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


def getReaction(request):
    if 'id' in request.GET:
        id = request.GET['id']
        sample = Live.objects.values_list('liveId',flat=True)
        print(sample)
        if id in Live.objects.values_list('liveId', flat=True):
            l = get_object_or_404(Live, liveId=id)
            choiced_reaction = l.reactions_set.all()

            for react in choiced_reaction:
                if react.reactionCount % 10 == 0:
                    sendreaction = react.reaction
                    message = 'success'

                    params = {
                        'Reaction':sendreaction,
                        'message':message,
                    }

                    json_str=json.dumps(params, ensure_ascii=False, indent=2)
                    return HttpResponse(json_str)
                else:
                    sendreaction='NA'
                    message='no reactions'

                    params = {
                        'Reaction': sendreaction,
                        'message':message,
                    }

                    json_str=json.dumps(params, ensure_ascii=False, indent=2)


        else:
            params={
                'Reaction':'NA',
                'message':'do not exist such a video'
            }
            json_str = json.dumps(params, ensure_ascii=False, indent=2)            
    else:
        params={
        'Reaction':'NA',
        'message':'input id'
        }
        json_str = json.dumps(params, ensure_ascii=False, indent=2)
    
    return HttpResponse(json_str)
