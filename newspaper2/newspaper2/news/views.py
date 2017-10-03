from datetime import datetime

from django.conf import settings # La manera correcta de importar settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView

from rest_framework import generics as rfapiviews  #Utilizo un nombre mas facilito para generics
from rest_framework.pagination import PageNumberPagination

from newspaper2.news.forms import NewsForm, EventForm
from newspaper2.news.models import News, Event
from newspaper2.news.serializers import NewsSerializer, NewsSerializerComplete


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


def news(request, newsitem_pk):
    news_filtered = News.objects.published()
    news_item = get_object_or_404(news_filtered, pk=newsitem_pk)

    return render(request, 'news/news.html',
        {'news_item': news_item})


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
        messages.success(request, _('News successfully added'))  #Con el guion bajo preparamos para traducir
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
        messages.success(request, _('News successfully edited'))
        return HttpResponseRedirect(reverse('news_list'))
    return render(request, 'news/news_edit.html',
        {'news_form': news_form})


@login_required(login_url='/admin/')
def news_delete(request, newsitem_pk):
        if request.method != 'POST':
            return HttpResponseBadRequest(_('Invalid Request'))
        news_item = get_object_or_404(News, pk=newsitem_pk)
        news_item.delete()
        messages.success(request, _('News successfully deleted'))
        return HttpResponseRedirect(reverse('news_list'))


def events_list(request):
    events = Event.objects.filter(
        publish_date__lte=datetime.now()).order_by('-publish_date')
    return render(request, 'news/events_list.html',
        {'events': events})


def event(request, event_pk):
    events_filtered = Event.objects.filter(
        publish_date__lte=datetime.now()).order_by('-publish_date')
    event = get_object_or_404(events_filtered, pk=event_pk)

    return render(request, 'news/event.html',
        {'event': event})


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
        messages.success(request, _('Event successfully added'))
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
        messages.success(request, _('Event successfully edited'))
        return HttpResponseRedirect(reverse('events_list'))
    return render(request, 'news/event_edit.html',
        {'event_form': event_form})


@login_required(login_url='/admin/')
def event_delete(request, event_pk):
        if request.method != 'POST':
            return HttpResponseBadRequest(_('Invalid Request'))
        event = get_object_or_404(Event, pk=event_pk)
        event.delete()
        messages.success(request, _('Event successfully deleted'))
        return HttpResponseRedirect(reverse('events_list'))


class BaseNews(object):
    model = News


class NewsListView(BaseNews, ListView):
    template_name = 'news/news_list.html'
    model = News
    context_object_name = 'news'  #Es el nombre del contexto (los datos) que le pasamos a la plantilla (Como en los render)

    def get_queryset(self):
        #Modifica la consulta normal (self.model.objects.all()) para que utilice el manager published()
        return self.model.objects.published()


class NewsAddView(BaseNews, CreateView):
    model = News
    form = NewsForm
    template_name = 'news/news_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('news_list_v2')

    #La plantilla espera que le pasemos news_form (como nombre del contexto) pero por defecto esta clase le pasa form.
    #Con este metodo, conseguimos pasar el formulario como news_form en vez de como form.
    def get_context_data(self, *args, **kwargs):
        ctx = super(NewsAddView, self).get_context_data(*args, **kwargs)
        ctx['news_form'] = ctx['form']
        return ctx


class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class NewsListAPI(rfapiviews.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer  #Llamo al seralizador para transformar la query en json
    pagination_class = NewsPagination
    filter_fields = ('title',)  #Incluimos un filtro (http://85.214.225.9:8000/api/news/?title=Mi noticia) sobre el titulo


class NewsAddAPI(rfapiviews.CreateAPIView):
    model = News
    serializer_class = NewsSerializerComplete
