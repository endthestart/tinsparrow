import getpass
import sys
import time
import logging

import json
import requests

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from library import Library
from importer import Importer
from uploader import Uploader

engine = create_engine('sqlite:///tinsparrow.db', echo=True)

# TODO: This should become a configuration
SCAN_ON_START = True
LIBRARY_PATH = '/Users/manderson/Music'
API_AUTH_URL = 'http://localhost:8000/api/token-auth/'

def main():
    token = login()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    library = session.query(Library).filter_by(path=LIBRARY_PATH).first()
    if not library:
        library = Library()
        library.path = LIBRARY_PATH
        session.add(library)

    session.commit()

    importer = Importer()
    importer.find_media(session, library)

    session.commit()

    uploader = Uploader()
    uploader.sync(session, token)

    session.commit()

    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d $H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # event_handler = LoggingEventHandler()
    # observer = Observer()
    # observer.schedule(event_handler, path, recursive=True)
    # observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()

def login():
    username = raw_input("Email: ")
    password = getpass.getpass()

    return authenticate(username=username, password=password)


def authenticate(username, password):
    auth_r = requests.post(API_AUTH_URL, data={'username': username, 'password': password})
    if auth_r.status_code == 200:
        token_json = json.loads(auth_r.content)
        token = token_json.get('token', None)
        if token:
            return token
    else:
        login()


if __name__ == "__main__":
    main()



