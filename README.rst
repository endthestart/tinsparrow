========================
Tin Sparrow
========================

A Django, Django Rest Framework, and Backbone music manager and player.

========================
Setup
========================

 # Configure your virtualenv (mkvirtualenv tinsparrow)
 # pip install -r requirements/local.py
 # ./manage.py syncdb
 # ./manage.py migrate
 # ./manage.py runserver
 
In the admin (/admin/) you can add a Library and point it to a path on the local filesystem that contains music.
After adding a library you can sync the database with music.

 # ./manage.py import_media
 
========================
API
========================

The API can be found at the /api/ url and comtains some links to browse it.
