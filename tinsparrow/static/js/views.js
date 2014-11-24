(function ($, Backbone, _, app) {
    var TemplateView = Backbone.View.extend({
        templateName: '',
        initialize: function () {
            this.template = _.template($(this.templateName).html());
        },
        render: function () {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function () {
            return {};
        }
    });

    var LibraryView = TemplateView.extend({
        templateName: '#library-template',
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            app.collections.ready.done(function () {
                app.artists.fetch({
                    success: $.proxy(self.render, self)
                });
            });
        },
        getContext: function () {
            return {artists: app.artists || null}
        }
    });

    var ArtistDetailView = TemplateView.extend({
        templateName: '#artist-detail-template',
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            this.artistId = options.artistId;
            this.artist = null;
            this.albums = [];
            this.songs = [];
            app.collections.ready.done(function () {
                app.albums.on('add', self.addAlbum, self);
                app.songs.on('add', self.addSong, self);
                self.artist = app.artists.push({id: self.artistId});
                self.artist.fetch({
                    success: function () {
                        self.render();
                        app.albums.each(self.addAlbum, self);
                        self.artist.fetchAlbums();
                        app.songs.each(self.addSong, self);
                        self.artist.fetchSongs();
                    }
                });
            });
        },
        getContext: function () {
            return {artist: this.artist};
        },
        addAlbum: function (album) {
            if (album.inArtist(this.artist)) {
                this.albums[album.get('id')] = album;
                this.renderAlbum(album);
            }

        },
        renderAlbum: function (album) {
            var container = this,
                data = {"album": album},
                template = _.template('<li><a href="#album/<%- album.get("id") %>" class="album"><%- album.get("title") %></a></li>');
            $('.albums', container.$el).append(template(data));
        },
        addSong: function (song) {
            if (song.inArtist(this.artist)) {
                this.songs[song.get('id')] = song;
                this.renderSong(song);
            }
        },
        renderSong: function (song) {
            var container = this,
                data = {"song": song},
                template = _.template('<li><a href="#" class="song"><%- song.get("title") %></a></li>');
            $('.songs', container.$el).append(template(data));
        }
    });

    var AlbumListView = TemplateView.extend({
        templateName: '#album-list-template',
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            app.collections.ready.done(function () {
                app.albums.fetch({
                    success: $.proxy(self.render, self)
                });
            });
        },
        getContext: function () {
            return {albums: app.albums || null}
        }
    });

    var AlbumDetailView = TemplateView.extend({
        templateName: '#album-detail-template',
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            this.albumId = options.albumId;
            this.album = null;
            this.songs = []
            app.collections.ready.done(function () {
                app.songs.on('add', self.addSong, self);
                self.album = app.albums.push({id: self.albumId});
                self.album.fetch({
                    success: function () {
                        self.render();
                        app.songs.each(self.addSong, self);
                        self.album.fetchSongs();
                    }
                });
            });
        },
        getContext: function () {
            return {album: this.album};
        },
        addSong: function (song) {
            if (song.inAlbum(this.album)) {
                this.songs[song.get('id')] = song;
                this.renderSong(song);
            }
        },
        renderSong: function (song) {
            var container = this,
                data = {"song": song},
                template = _.template('<li><a href="#" class="song"><%- song.get("title") %></a></li>');
            $('.songs', container.$el).append(template(data));
        }
    });

    var SongListView = TemplateView.extend({
        templateName: '#song-list-template',
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            app.collections.ready.done(function () {
                app.songs.fetch({
                    success: $.proxy(self.render, self)
                });
            });
        },
        getContext: function () {
            return {songs: app.songs || null}
        }
    });

    var ArtistSongListView = TemplateView.extend({
        templateName: '#artist-song-list-template'
    });

    var QueueView = TemplateView.extend({
        templateName: '#queue-template',
        initialize: function (options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            app.collections.ready.done(function() {
                app.queue.fetch({
                    success: $.proxy(self.render, self)
                });
            })
        },
        getContext: function () {
            return {songs: app.queue.models}
        }
    });

    app.views.LibraryView = LibraryView;
    app.views.ArtistDetailView = ArtistDetailView;
    app.views.AlbumListView = AlbumListView;
    app.views.AlbumDetailView = AlbumDetailView;
    app.views.SongListView = SongListView;
    app.views.ArtistSongListView = ArtistSongListView;
    app.views.QueueView = QueueView;
})(jQuery, Backbone, _, app);