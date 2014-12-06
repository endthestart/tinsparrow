import json
import os
import requests

from urlparse import urljoin

from library import Song

API_URL = 'http://localhost:8000/api/'

class Uploader(object):
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': 'Token {}'.format(token)}


    def sync(self, session):
        """
        1. Select all songs in the database not uploaded
        2. Compare fingerprints with songs on server
        3. If not match try artist, album, and title together
        4. If not match then finally upload song as new file
        :param session:
        :return:
        """
        url = urljoin(API_URL, 'upload/')
        songs = session.query(Song).filter_by(uploaded=False)
        for song in songs:
            with open(os.path.join(song.path, song.filename)) as song_file:
                files = {os.path.join(song.path, song.filename): song_file}
                data = {
                    'artist': song.artist,
                    'album': song.album,
                    'title': song.title,
                    'track': song.track,
                    'length': song.length,
                }
                match = self.match_fingerprint(song.fingerprint)
                match_json = json.loads(match.content)
                if match_json.get('count', False):
                    # put the song into their library
                    song.uploaded = True
                else:
                    # We don't have a match, upload
                    upload_request = requests.post(
                        url,
                        headers=self.headers,
                        data=data,
                        files=files
                    )
                    song.uploaded = True
            # song.uploaded = True

    def match_fingerprint(self, fingerprint):
        url = urljoin(API_URL, 'songs/')
        payload = {'fingerprint': fingerprint}
        return requests.get(url, headers=self.headers, params=payload)

    def match_metadata(self):
        return False
