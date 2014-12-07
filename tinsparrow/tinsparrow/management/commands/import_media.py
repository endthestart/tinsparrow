from django.core.management.base import BaseCommand

from tinsparrow.importer import Importer
from tinsparrow.models import Library


class Command(BaseCommand):
    help = '''Add all media to the database'''

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        importer = Importer()
        library, _ = Library.objects.get_or_create()
        importer.find_media(library)
