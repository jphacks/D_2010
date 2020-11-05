import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Live
from django.utils import timezone

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


"""
def addVideos(request):
    if 'id' in request.GET and 'user' in request.GET:
        l = Live()
        liveUser = request.GET['user']
        liveId = request.GET['id']
        

        liveNameにliveId(YouTubeIDと同じ)からとってきたライブのタイトルをとってきてほしい
    
        liveName = 

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

"""
     