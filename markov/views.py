from django.shortcuts import render

from markov.models import User

def index(request):
  context = {}
  return render(request, 'markov/index.html', context)
