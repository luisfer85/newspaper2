from django.contrib import admin

from newspaper2.news.models import News

class NewsAdmin(admin.ModelAdmin):
	pass

admin.site.register(News, NewsAdmin)