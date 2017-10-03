from rest_framework import serializers

from newspaper2.news.models import News


class NewsSerializer(serializers.ModelSerializer):


    class Meta:
        model = News
        fields = ('title', 'publish_date')