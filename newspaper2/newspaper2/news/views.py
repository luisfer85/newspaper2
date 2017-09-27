from datetime import datetime

from django.conf import settings # La manera correcta de importar settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from newspaper2.news.forms import NewsForm, EventForm
from newspaper2.news.models import News, Event

def news_list(request):
    news_filtered = News.objects.published()
    paginator = Paginator(news_filtered, settings.PAGINATION_PAGES) # variable en settings.py
    page_default = 1

    page = request.GET.get('page', page_default)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(page_default)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return render(request, 'news/news_list.html',
        {'news': news})


@login_required(login_url='/admin/')
def news_add(request):
    if request.method == 'POST':
        data = request.POST
    else:
        data = None
    '''
    # Si queremos recoger el valor del title mediante GET
    if 'title' in request.GET:
        initial = {'title': request.GET['title']
    '''
    '''
    # Mas dificil todavia
    if 'name' in request.GET:
        initial = {'description': 'Estimado: %s' % request.GET['name']}
    '''
    initial = {'publish_date': datetime.now()}
    news_form = NewsForm(data=data,
        initial=initial) # Da un valor por defecto a publish_date
    if news_form.is_valid():
        news_form.save()
        messages.success(request, 'Noticia creada correctamente')
        return HttpResponseRedirect(reverse('news_list'))
    return render(request, 'news/news_edit.html',
        {'news_form': news_form})


@login_required(login_url='/admin/')
def news_edit(request, newsitem_pk):
    if request.method == 'POST':
        data = request.POST
    else:
        data = None
    news_item = get_object_or_404(News, pk=newsitem_pk)
    news_form = NewsForm(data=data,
        instance=news_item)
    if news_form.is_valid():
        news_form.save()
        messages.success(request, 'Noticia editada correctamente')
        return HttpResponseRedirect(reverse('news_list'))
    return render(request, 'news/news_edit.html',
        {'news_form': news_form})


@login_required(login_url='/admin/')
def news_delete(request, newsitem_pk):
        if request.method != 'POST':
            return HttpResponseBadRequest('Invalid Request')
        news_item = get_object_or_404(News, pk=newsitem_pk)
        news_item.delete()
        messages.success(request, 'Noticia eliminada correctamente')
        return HttpResponseRedirect(reverse('news_list'))


def events_list(request):
    events = Event.objects.filter(
        publish_date__lte=datetime.now()).order_by('-publish_date')
    return render(request, 'news/events_list.html',
        {'events': events})


@login_required(login_url='/admin/')
def event_add(request):
    if request.method == 'POST':
        data = request.POST
    else:
        data = None
    initial = {'publish_date': datetime.now()}
    event_form = EventForm(data=data,
        initial=initial) # Da un valor por defecto a publish_date
    if event_form.is_valid():
        event_form.save()
        messages.success(request, 'Evento creado correctamente')
        return HttpResponseRedirect(reverse('events_list'))
    return render(request, 'news/event_edit.html',
        {'event_form': event_form})


@login_required(login_url='/admin/')
def event_edit(request, event_pk):
    if request.method == 'POST':
        data = request.POST
    else:
        data = None
    event = get_object_or_404(Event, pk=event_pk)
    event_form = EventForm(data=data,
        instance=event)
    if event_form.is_valid():
        event_form.save()
        messages.success(request, 'Evento editado correctamente')
        return HttpResponseRedirect(reverse('events_list'))
    return render(request, 'news/event_edit.html',
        {'event_form': event_form})


@login_required(login_url='/admin/')
def event_delete(request, event_pk):
        if request.method != 'POST':
            return HttpResponseBadRequest('Invalid Request')
        event = get_object_or_404(Event, pk=event_pk)
        event.delete()
        messages.success(request, 'Evento eliminado correctamente')
        return HttpResponseRedirect(reverse('events_list'))