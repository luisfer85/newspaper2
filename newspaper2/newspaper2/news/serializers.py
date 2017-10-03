from django.core.urlresolvers import reverse

from rest_framework import serializers

from newspaper2.news.models import News


class NewsSerializer(serializers.ModelSerializer):

    href = serializers.SerializerMethodField('get_href_url')  #Lo definimos como un metodo y lo llamamos get_href_url

    class Meta:
        model = News
        fields = ('title', 'publish_date', 'href')

    def get_href_url(self, obj):
        url = reverse('news_detail_api', args=(obj.pk,))  #Conseguimos la ruta relativa (ej: /api/news/8/)
        return self.context.get('request').build_absolute_uri(url)  #Obtenemos el request de django y añadimos la ruta relativa


class NewsSerializerComplete(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('title', 'description', 'publish_date')
