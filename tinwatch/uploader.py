import os
import requests

from library import Song

API_URL = 'http://localhost:8000/api/upload/'

class Uploader(object):
    def sync(self, session, token):
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
            with open(os.path.join(song.path, song.filename)) as song_file:
                files = {os.path.join(song.path, song.filename): song_file}
                headers = {'Authorization': token}
                data = {
                    'artist': song.artist,
                    'album': song.album,
                    'title': song.title,
                    'track': song.track,
                    'length': song.length,
                }
                r = requests.post(
                    API_URL,
                    headers=headers,
                    data=data,
                    files=files
                )
            # song.uploaded = True

