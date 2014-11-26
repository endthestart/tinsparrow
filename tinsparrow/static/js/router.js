(function ($, Backbone, _, app) {
    var AppRouter = Backbone.Router.extend({
        routes: {
            '': 'library',
            'artists': 'library',
            'albums': 'albums',
            'songs': 'songs',
            'artists/:id': 'artist',
            'albums/:id': 'album',
            'queue': 'queue'
        },
        initialize: function (options) {
            this.contentElement = '.content';
            this.current = null;
            Backbone.history.start();
        },
        library: function() {
            var view = new app.views.LibraryView({
                el: this.contentElement
            });
            this.render(view);
        },
        albums: function() {
            var view = new app.views.AlbumListView({
                el: this.contentElement
            });
            this.render(view);
        },
        songs: function() {
            var view = new app.views.SongListView({
                el: this.contentElement
            });
            this.render(view);
        },
        artist: function(id) {
            var view = new app.views.ArtistDetailView({
                el: this.contentElement,
                artistId: id
            });
            this.render(view);
        },
        album: function(id) {
            var view = new app.views.AlbumDetailView({
                el: this.contentElement,
                albumId: id
            });
            this.render(view);
        },
        queue: function() {
            var view = new app.views.QueueView({
                el: this.contentElement
            });
            this.render(view);
        },
        render: function (view) {
            if (this.current) {
                this.current.$el = $();
                this.current.remove();
            }
            this.current = view;
            this.current.render();
        }
    });

    app.router = AppRouter;
})(jQuery, Backbone, _, app);
