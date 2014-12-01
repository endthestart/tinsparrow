import sys
import time
import logging

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .library import Library
from .importer import Importer

Base = declarative_base()
engine = create_engine('sqlite:///tinsparrow.db', echo=True)

# TODO: This should become a configuration
SCAN_ON_START = True


def main():
    Session = sessionmaker()
    Session.configure(bing=engine)
    session = Session()

    for instance in session.query(Library):
        Importer.find_media(instance)


    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d $H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()



