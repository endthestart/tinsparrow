import sys
import time
import logging

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


def main():
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
    uploader.sync(session)

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


if __name__ == "__main__":
    main()



