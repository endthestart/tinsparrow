import getpass
import sys
import shelve
import time
import logging
import os
from urlparse import urljoin

import json
import requests

import Tkinter as tk
import tkFileDialog as tfile

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from library import Library, get_or_create
from importer import Importer
from uploader import Uploader
from settings import *

# TODO: Figure out how to create database first time and migrations
engine = create_engine('sqlite:///tinsparrow.db', echo=False)


class TinWatch(object):
    def __init__(self):
        # TODO: Convert to PySide GUI Application
        # Currently using tkinter because it's easy
        self.session = self.create_db_session()

    def create_db_session(self):
        Session = sessionmaker()
        Session.configure(bind=engine)
        return Session()

    def main(self):
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()
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

class SettingsWindow(tk.Tk):
    def __init__(self, root):
        root.title('Settings')
        root.geometry('600x320')
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        self.root = root
        self.parent = frame
        self.initialize()

    def initialize(self):
        self.file_label = tk.Label(self.parent, text="Set a directory to scan.")
        self.file_label.pack()
        self.file_button = tk.Button(self.parent, text="Add Music", command=self.ask)
        self.file_button.pack()
        self.listbox = tk.Listbox(self.parent)
        self.listbox.pack()
        self.save_button = tk.Button(self.parent, text="Save", command=self.save)
        self.save_button.pack()
        self.refresh_listbox()

    def ask(self):
        music_path = tfile.askdirectory(parent=self.parent)
        self.add_music_directory(music_path)

    def add_music_directory(self, music_path=None):
        if not os.path.isdir(music_path):
            return
        library = get_or_create(self.session, Library, path=music_path)
        self.session.commit()
        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        self.libraries = tw.session.query(Library).all()
        for library in self.libraries:
            self.listbox.insert(tk.END, library.path)

    def save(self):
        self.parent.destroy()
        MonitorWindow(self.root)


class MonitorWindow(tk.Tk):
    def __init__(self, root):
        root.title('Monitor')
        root.geometry('600x320')
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        self.root = root
        self.parent = frame
        self.initialize()

    def initialize(self):
        self.settings_button = tk.Button(self.parent, text="Settings", command=self.open_settings)
        self.settings_button.pack()

    def open_settings(self):
        self.parent.destroy()
        SettingsWindow(self.root)


class LoginWindow(tk.Tk):
    def __init__(self, root):
        root.title('Login')
        root.geometry('300x160')
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        self.parent = frame
        self.root = root
        self.user_string = tk.StringVar()
        self.password_string = tk.StringVar()
        self.app_config = shelve.open(CONFIG)
        self.initialize()

    def initialize(self):
        if self.check_token(self.app_config.get('token', False)):
            self.open_monitor()
        else:
            self.user_label = tk.Label(self.parent, text="Username: ")
            self.user_label.pack()
            self.user_entry = tk.Entry(self.parent, textvariable=self.user_string)
            self.user_entry.pack()
            self.password_label = tk.Label(self.parent, text="Password: ")
            self.password_label.pack()
            self.password_entry = tk.Entry(self.parent, show="*", textvariable=self.password_string)
            self.password_entry.pack()
            self.login_button = tk.Button(self.parent, borderwidth=4, text="Login", width=10, pady=8, command=self.act)
            self.login_button.pack(side=tk.BOTTOM)
            self.password_entry.bind('<Return>', self.enter)
            self.user_entry.focus_set()

    def act(self):
        token = self.authenticate(self.user_string.get(), self.password_string.get())
        if token:
            self.app_config['token'] = token
            self.open_settings()
        else:
            self.root.title('Login Failure: Try again...')

    def open_settings(self):
        self.app_config.close()
        self.parent.destroy()
        SettingsWindow(self.root)

    def open_monitor(self):
        self.app_config.close()
        self.parent.destroy()
        MonitorWindow(self.root)

    def enter(self, event):
            self.act()

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

    def check_token(self, token):
        # TODO: This can be used to check internet connectivity?
        url = API_URL
        headers = {'Authorization': 'Token {}'.format(token)}
        auth_r = requests.get(url, data={}, headers=headers)
        if auth_r.status_code == 200:
            return True
        else:
            return False

if __name__ == "__main__":
    tw = TinWatch()
    tw.main()
