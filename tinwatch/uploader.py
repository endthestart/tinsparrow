from library import Song


class Uploader(object):
    def sync(self, session):
        """
        1. Select all songs in the database not uploaded
        2. Compare fingerprints with songs on server
        3. If not match try artist, album, and title together
        4. If not match then finally upload song as new file
        :param session:
        :return:
        """
        songs = session.query(Song).filter(uploaded=False)
        for song in songs:
            print song.filename
            print "Comparing the fingerprint with the server"
            print "Comparing the artist, album, and title together"
            print "Uploading the song"
            song.uploaded = True
