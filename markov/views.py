from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.conf import settings

from markov.models import User, MarkovBot, GroupMeInterface

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
  groups = GroupMeInterface.get_groups(access_token)
  #Train on messages from all groups
  m = []
  for group in groups:
    m.extend(GroupMeInterface.get_all_messages(access_token, group['id'])) 
  sen = GroupMeInterface.get_sentences(m)
  bot = MarkovBot()
  bot.train(sen)
  predicted = []
  for x in range(0, 100):
    predicted.append(bot.generate_sentence())
  context = {'access_token': user.access_token, 'predicted': predicted}
  return render(request, 'markov/prediction.html', context)

def prediction(request):
  context = {'access_token': access_token}
  return render(request, 'markov/prediction.html', context)  