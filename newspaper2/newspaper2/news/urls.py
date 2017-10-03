"""newspaper2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from newspaper2.news import views

urlpatterns = [
    url(r'^$', views.news_list, name='news_list'),
    url(r'^news/$', views.news_list, name='news_list'),
    url(r'^news/news/(?P<newsitem_pk>\d+)/$', views.news, name='news'),
    url(r'^news/add/$', views.news_add, name='news_add'),
    url(r'^news/edit/(?P<newsitem_pk>\d+)/$', views.news_edit, name='news_edit'),
    url(r'^news/delete/(?P<newsitem_pk>\d+)/$', views.news_delete, name='news_delete'),
    url(r'^events/$', views.events_list, name='events_list'),
    url(r'^events/event/(?P<event_pk>\d+)/$', views.event, name='event'),
    url(r'^events/add/$', views.event_add, name='event_add'),
    url(r'^events/edit/(?P<event_pk>\d+)/$', views.event_edit, name='event_edit'),
    url(r'^events/delete/(?P<event_pk>\d+)/$', views.event_delete, name='event_delete'),
    url(r'^v2/$', views.NewsListView.as_view(), name='news_list_v2'),
    url(r'^v2/news/add/$', views.NewsAddView.as_view(), name='news_add_v2'),
    url(r'^api/news/$', views.NewsListAPI.as_view(), name='news_list_api'),
    url(r'^api/news/add/$', views.NewsAddAPI.as_view(), name='news_add_api'),
]
