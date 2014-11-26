from django.conf.urls import url

from markov import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
