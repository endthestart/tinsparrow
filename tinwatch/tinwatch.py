import getpass
import sys
import time
import logging
from urlparse import urljoin

import json
import requests

import Tkinter as tk

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from library import Library
from importer import Importer
from uploader import Uploader
from settings import *

# TODO: Figure out how to create database first time and migrations
engine = create_engine('sqlite:///tinsparrow.db', echo=False)


class TinWatch(object):
    def main(self):
        self.login()
        # return False
        # token = login()
        # Session = sessionmaker()
        # Session.configure(bind=engine)
        # session = Session()
        #
        # library = session.query(Library).filter_by(path=LIBRARY_PATH).first()
        # if not library:
        #     library = Library()
        #     library.path = LIBRARY_PATH
        #     session.add(library)
        #
        # session.commit()
        #
        # importer = Importer()
        # importer.find_media(session, library)
        #
        # session.commit()
        #
        # uploader = Uploader(token)
        # uploader.sync(session)
        #
        # session.commit()

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

    def enter(self, event):
        self.act()

    def login(self):
        self.root = tk.Tk()
        self.root.geometry('300x160')
        self.root.title('Login')
        parent = tk.Frame(self.root, padx=10, pady=10)
        parent.pack(fill=tk.BOTH, expand=True)
        self.user_string = tk.StringVar()
        self.password_string = tk.StringVar()
        user_label = tk.Label(parent, text="Username: ")
        user_label.pack()
        user_entry = tk.Entry(parent, textvariable=self.user_string)
        user_entry.pack()
        password_label = tk.Label(parent, text="Password: ")
        password_label.pack()
        password_entry = tk.Entry(parent, show="*", textvariable=self.password_string)
        password_entry.pack()
        login_button = tk.Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=self.act)
        login_button.pack(side=tk.BOTTOM)
        password_entry.bind('<Return>', self.enter)
        user_entry.focus_set()
        parent.mainloop()

    def act(self):
        self.token = self.authenticate(self.user_string.get(), self.password_string.get())
        if self.token:
            self.root.destroy()
            print self.token
        else:
            self.root.title('Login Failure: Try again...')

    def authenticate(self, username, password):
        url = urljoin(API_URL, 'token-auth/')
        auth_r = requests.post(url, data={'username': username, 'password': password})
        if auth_r.status_code == 200:
            token_json = json.loads(auth_r.content)
            token = token_json.get('token', None)
            if token:
                return token
        else:
            return False


if __name__ == "__main__":
    tw = TinWatch()
    tw.main()



