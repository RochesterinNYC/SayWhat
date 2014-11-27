from django.conf.urls import url

from markov import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth', views.auth, name='auth'),
    url(r'^callback', views.callback, name='callback'),
    url(r'^prediction', views.prediction, name='prediction'),
]
