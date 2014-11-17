from django.core.management.base import BaseCommand

from tinsparrow.models import Artist, Album, Song


class Command(BaseCommand):
    help = '''Deletes all media from the database'''

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        Song.objects.all().delete()
        Album.objects.all().delete()
        Artist.objects.all().delete()