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
        songs = session.query(Song).filter_by(uploaded=False)
        for song in songs:
            # TODO: reorganize these if statements?
            fingerprint_match, match_id = self.match_fingerprint(song.fingerprint)
            if fingerprint_match:
                self.add_song_id_to_library(match_id)
            else:
                metadata_match, match_id = self.match_metadata(song)
                if metadata_match:
                    self.add_song_id_to_library(match_id)
                else:
                    self.upload_song(song)

    def match_fingerprint(self, fingerprint):
        # TODO: match fingerprint and metadata could be one method. If kwargs['fingerprint'] or if kwargs other data, etc.
        match_found = False
        match_id = None

        url = urljoin(API_URL, 'songs/')
        payload = {'fingerprint': fingerprint}
        match = requests.get(url, headers=self.headers, params=payload)
        match_json = json.loads(match.content)

        if match_json.get('count') > 0:
            match_found = True
            match_id = match_json['results'][0]['id']

        return match_found, match_id

    def match_metadata(self, song):
        match_found = False
        match_id = None

        url = urljoin(API_URL, 'songs/')
        payload = {
            'artist': song.artist,
            'album': song.album,
            'title': song.title,
        }
        match = requests.get(url, headers=self.headers, params=payload)
        match_json = json.loads(match.content)

        if match_json.get('count') > 0:
            match_found = True
            match_id = match_json['results'][0]['id']

        return match_found, match_id

    def add_song_id_to_library(self, song_id):
        url = urljoin(API_URL, 'library/')
        data = {
            'id': song_id,
        }
        add_request = requests.post(
            url,
            headers=self.headers,
            data=data
        )
        return False

    def upload_song(self, song):
        url = urljoin(API_URL, 'upload/')
        with open(os.path.join(song.path, song.filename)) as song_file:
            files = {
                os.path.join(song.path, song.filename): song_file
            }
            data = {
                'artist': song.artist,
                'album': song.album,
                'title': song.title,
                'track': song.track,
                'length': song.length,
            }
            upload_request = requests.post(
                url,
                headers=self.headers,
                data=data,
                files=files
            )
