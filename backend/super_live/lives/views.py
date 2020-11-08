import json
import urllib.parse

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Live, Reactions
from django.utils import timezone
from apiclient.discovery import build



DEVELOPER_KEY = "API Key" #Youtube API Keyを入れるところ
reactionSet = ['happy', 'sad', 'wow']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


#viewとはあまり関係がない関数
def min(a):
    if a <= 11:
        return 11
    else:
        return a


def SearchVideos(request):
    if 'name' in request.GET:
        name = request.GET['name']
        name = urllib.parse.unquote(name)
        memo_list=[]
        result_list = []

        for name_str in Live.objects.values_list("liveName", flat=True):
            for result_name in Live.objects.filter(liveName=name):
                if result_name.liveId not in memo_list:
                    memo_list.append(result_name.liveId)
                    name = result_name.liveUser
                    param = {
                        'id': result_name.liveID,
                        'videoTitle':result_name.liveName,
                    }
                    result_list.append(param)
                    message = 'success'

        for name_str in Live.objects.values_list("liveUser", flat=True):
            for result_user in Live.objects.filter(liveUser=name):
                if result_user.liveId not in memo_list:
                    memo_list.append(result_user.liveId)
                    param = {
                        'id':result_user.liveId,
                        'videoTitle':result_user.liveName,
                    }
                    result_list.append(param)
                    message = 'success'

        if (name not in Live.objects.values_list("liveName", flat=True) and (name not in Live.objects.values_list("liveUser", flat=True))):
            liveId='NA'
            message = 'do not exist such a live'
    
    else:
        name='NA'
        liveId='NA'
        message='send live name'
    
    params={
        'name':name,
        'videos':result_list,
        'message':message,
    }

    
    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)



def SearchYtId(request):
    if 'name' in request.GET:
        name = request.GET['name']
        name = urllib.parse.unquote(name)
        for name_str in Live.objects.values_list("liveName", flat=True):
            if name in name_str:
                liveId = ', '.join([q.liveId for q in Live.objects.filter(liveName=name)])
                pub_data = timezone.now()
                message = 'success'
                
        for name_str in Live.objects.values_list("liveUser", flat=True):
            if name in name_str:
                liveId = ', '.join([q.liveId for q in Live.objects.filter(liveUser=name)])
                pub_data = timezone.now()
                message = 'success'

        if (name not in Live.objects.values_list("liveName", flat=True)) and (name not in Live.objects.values_list("liveUser", flat=True)):
            liveId='NA'
            pub_data = 'NA'
            message = 'do not exist such a live'
    
    else:
        name='NA'
        liveId='NA'
        pub_data='NA'
        message='send live name'
    
    params={
        'name':name,
        'id':liveId,
        'message':message,
    }

    
    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)


def addVideos(request):

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
            l.reactions_set.create(reaction=re, reactionCount=1)

        message = 'success'
    
    else:
        message='fauler'

    params={
        'message':message,
    }

    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)


def setReaction(request):
    print(request.method)
    if 'id' in request.GET:
        id = request.GET['id']
        re = request.GET['reaction']
        if id in Live.objects.values_list('liveId', flat=True) and re in reactionSet:
            l = get_object_or_404(Live, liveId = id)
            try:
                selected_reaction = l.reactions_set.get(reaction=re)
            except (KeyError, Reactions.DoNotExist):
                message = '1failure'
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
            message = '2failure'
            params = {
                'message':message,
            }
            json_str = json.dumps(params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str)
    else:
        message = '3failure'
        params = {
            'message':message,
        }
        json_str = json.dumps(params, ensure_ascii=False, indent=2)
        return HttpResponse(json_str)


def getReaction(request):
    if 'id' in request.GET:
        liveId = request.GET['id']
        if liveId in Live.objects.values_list('liveId', flat=True):
            l = get_object_or_404(Live, liveId=liveId)
            choiced_reaction = l.reactions_set.all()
#           視聴者数で決める場合

#            youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY,cache_discovery=False)
#            response = youtube.videos().list(part="snippet,liveStreamingDetails",id=liveId).execute()
#            liveName = response["items"][0]["snippet"]["title"]
#            viewer = response["items"][0]["liveStreamingDetails"]["concurrentViewers"]
            
            for react in choiced_reaction:
                if react.reactionCount % 3 == 0:
                    react.reactionCount += 1
                    react.save()
                    sendreaction = react.reaction
                    message = 'success'

                    params = {
                        'reaction':sendreaction,
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
