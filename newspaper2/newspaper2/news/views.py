from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from newspaper2.news.forms import NewsForm
from newspaper2.news.models import News

def news_list(request):
	news = News.objects.filter(
		publish_date__lte=datetime.now()).order_by('-publish_date')
	return render(request, 'news/news_list.html',
		{'news': news})


def news_add(request):
	if request.method == 'POST':
		data = request.POST
	else:
		data = None
	news_form = NewsForm(data=data)
	if news_form.is_valid():
		news_form.save()
		return HttpResponseRedirect('../')
	return render(request, 'news/news_add.html',
		{'news_form': news_form})


def news_edit(request, newsitem_pk):
	pass