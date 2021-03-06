(function ($, Backbone, _, app) {
    var BaseModel = Backbone.Model.extend({
        url: function () {
            var links = this.get('links'),
                url = links && links.self;
            if (!url) {
                url = Backbone.Model.prototype.url.call(this);
            }
            return url;
        }
    });

    var BaseCollection = Backbone.Collection.extend({
        parse: function (response) {
            this._next = response.next;
            this._previous = response.previous;
            this._count = response.count;
            return response.results || [];
        }
        //    TODO: Add a getOrFetch method here maybe
    });

    app.models.Artist = BaseModel.extend({
        fetchAlbums: function () {
            var albums = this.get('albums');
            if (albums) {
                app.albums.fetch({url: albums, remove: false});
            }
        },
        fetchSongs: function () {
            var songs = this.get('songs');
            if (songs) {
                app.songs.fetch({url: songs, remove: false});
            }
        }
    });
    app.models.Album = BaseModel.extend({
        fetchSongs: function () {
            var songs = this.get('songs');
            if (songs) {
                app.songs.fetch({url: songs, remove: false});
            }
        },
        inArtist: function (artist) {
            return artist.get('id') == this.get('artist');
        }
    });
    app.models.Song = BaseModel.extend({
        inArtist: function (artist) {
            return artist.get('id') == this.get('artist').id;
        },
        inAlbum: function (album) {
            return album.get('id') == this.get('album').id;
        }
    });
    app.models.Queue = BaseModel.extend({});

    app.collections.ready = $.getJSON(app.apiRoot);
    app.collections.ready.done(function (data) {
        app.collections.Artists = BaseCollection.extend({
            model: app.models.Artist,
            url: data.artists
        });
        app.artists = new app.collections.Artists();

        app.collections.Albums = BaseCollection.extend({
            model: app.models.Album,
            url: data.albums
        });
        app.albums = new app.collections.Albums();

        app.collections.Songs = BaseCollection.extend({
            model: app.models.Song,
            url: data.songs
        });
        app.songs = new app.collections.Songs();

        app.collections.Queues = BaseCollection.extend({
            model: app.models.Song,
            url: data.queue,
            currentSong: null,
            initialize: function () {
                var self = this;
                this.$player = $('#audio-player');
                this.audioPlayer = this.$player.get(0);
                this.audioPlayer.addEventListener('ended', function (event) {
                    if (self.currentSong !== null) {
                        self.playNextSong(event);
                    }
                });
            },
            save: function (attributes, options) {
                var queueData = {'song_list': JSON.stringify(this.toJSON())};
                var self = this;
                $.ajax({
                    type: "POST",
                    url: data.queue,
                    data: queueData,
                    dataType: "json",
                    crossDomain: false,
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    success: function () {
                        self.fetch({
                            success: function () {
                                if (self.currentSong === null) {
                                    self.playQueue();
                                }
                                ;
                            }
                        });
                    }
                });

            },
            playQueue: function () {
                if (this.currentSong === null) {
                    var song = this.at(0);
                    this.currentSong = song.get('id');
                    this.$player.empty().append(
                        '<source src="' + song.get('song_url') + '" type="' + song.get('content_type') + '">'
                    );
                    this.audioPlayer.load();
                    this.audioPlayer.play();
                    console.log("Starting the queue.");
                } else {
                    if (this.audioPlayer.paused) {
                        this.audioPlayer.play();
                        console.log("Playing current song.");
                    } else {
                        this.audioPlayer.pause();
                        console.log("Pausing current song.");
                    }
                }
            },
            playNextSong: function () {
                if (this.currentSong === null) {
                    this.playQueue();
                } else {
                    var currentSong = app.queue.get({'id': app.queue.currentSong});
                    var nextSongIndex = app.queue.indexOf(currentSong) + 1;
                    var song = app.queue.at(nextSongIndex);
                    this.currentSong = song.get('id');
                    console.log(song);
                    this.$player.empty().append(
                        '<source src="' + song.get('song_url') + '" type="' + song.get('content_type') + '">'
                    );
                    this.audioPlayer.load();
                    this.audioPlayer.play();
                }
            },
            playPreviousSong: function () {
                if (this.currentSong === null) {
                    this.playQueue();
                } else {
                    var currentSong = app.queue.get({'id': app.queue.currentSong});
                    var nextSongIndex = app.queue.indexOf(currentSong) - 1;
                    var song = app.queue.at(nextSongIndex);
                    this.currentSong = song.get('id');
                    console.log(song);
                    this.$player.empty().append(
                        '<source src="' + song.get('song_url') + '" type="' + song.get('content_type') + '">'
                    );
                    this.audioPlayer.load();
                    this.audioPlayer.play();
                }
            }
        });
        app.queue = new app.collections.Queues();
    });

})(jQuery, Backbone, _, app);
