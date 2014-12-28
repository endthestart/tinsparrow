from .local import *

DATABASES['default']['NAME'] = normpath(join(DJANGO_ROOT, 'chris.db'))
