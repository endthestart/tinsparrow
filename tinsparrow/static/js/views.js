(function($, Backbone, _, app) {
    var LibraryView = Backbone.View.extend({
        templateName: '#library-template',
        initialize: function() {
            this.template = _.template($(this.templateName).html());
        },
        render: function() {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function() {
            return {};
        }
    });

    var ArtistListView = Backbone.View.extend({
        templateName: '#artist-list-template',
        initialize: function() {
            this.template = _.template($(this.templateName).html());
        },
        render: function() {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function() {
            return {};
        }
    });

    var ArtistDetailView = Backbone.View.extend({
        templateName: '#artist-detail-template',
        initialize: function() {
            this.template = _.template($(this.templateName).html());
        },
        render: function() {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function() {
            return {};
        }
    });

    var AlbumListView = Backbone.View.extend({
        templateName: '#album-list-template',
        initialize: function() {
            this.template = _.template($(this.templateName).html());
        },
        render: function() {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function() {
            return {};
        }
    });

    var AlbumDetailView = Backbone.View.extend({
        templateName: '#album-detail-template',
        initialize: function() {
            this.template = _.template($(this.templateName).html());
        },
        render: function() {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function() {
            return {};
        }
    });

    var SongListView = Backbone.View.extend({
        templateName: '#song-list-template',
        initialize: function() {
            this.template = _.template($(this.templateName).html());
        },
        render: function() {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function() {
            return {};
        }
    });

    var ArtistSongListView = Backbone.View.extend({
        templateName: '#artist-song-list-template',
        initialize: function() {
            this.template = _.template($(this.templateName).html());
        },
        render: function() {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function() {
            return {};
        }
    });

    app.views.LibraryView = LibraryView;
    app.views.ArtistView = ArtistListView;
    app.views.ArtistDetailView = ArtistDetailView;
    app.views.AlbumListView = AlbumListView;
    app.views.AlbumDetailView = AlbumDetailView;
    app.views.SongListView = SongListView;
    app.views.ArtistSongListView = ArtistSongListView;
})(jQuery, Backbone, _, app);