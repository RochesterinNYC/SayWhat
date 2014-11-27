from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.conf import settings

from markov.models import User

def index(request):
  context = {'token': settings.GROUPME_API_TOKEN}
  return render(request, 'markov/index.html', context)

def auth(request):
  return HttpResponseRedirect("https://api.groupme.com/oauth/authorize?client_id={}".format(settings.GROUPME_API_TOKEN))

def callback(request):
  access_token = request.GET.get('access_token','')
  try:
    user = User.objects.get(access_token=access_token)
  except User.DoesNotExist:
    user = User(access_token=access_token)
    user.save()
  context = {'access_token': user.access_token}
  return render(request, 'markov/prediction.html', context)

def prediction(request):
  context = {'access_token': access_token}
  return render(request, 'markov/prediction.html', context)  