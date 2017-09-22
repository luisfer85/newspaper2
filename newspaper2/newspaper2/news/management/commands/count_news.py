from django.core.management.base import BaseCommand, CommandError

from newspaper2.news.models import News

class Command(BaseCommand):
    help = 'Count news.'
    
    def handle(self, *args, **options):
        print(News.objects.count())