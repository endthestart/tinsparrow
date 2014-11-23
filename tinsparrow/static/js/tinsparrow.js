var app = (function ($) {
    var app = {
        "models": {},
        "collections": {},
        "views": {},
        "router": null
    };

    $(document).ready(function() {
        var router = new app.router();
    });

    return app;
})(jQuery);

//var SONG_SELECTOR = '.js-song',
//    PLAYER_SELECTOR = '#audio-player';
//
//QueueView = Backbone.View.extend({
//    el: '.js-queue-list',
//    events: {
//        "click .js-song": "playSong"
//    },
//    initialize: function () {
//        this.$player = $(PLAYER_SELECTOR);
//        this.$songs = this.$el.find(SONG_SELECTOR);
//        this.audioPlayer = this.$player.get(0);
//    },
//    playSong: function () {
//        var $song = $(event.target);
//
//        this.$songs.removeClass('active');
//        $song.addClass('active');
//
//        this.$player.empty().append(
//            '<source src="' + $song.data('url') + '" type="audio/mp4">'
//        );
//
//        this.audioPlayer.load();
//        this.audioPlayer.play();
//    }
//});
//
//qv = new QueueView();
//
//ArtistModel = Backbone.Model.extend({
//    urlRoot: '/api/artists',
//    url: function() {
//        return this.urlRoot + '/' + this.id + '/';
//    }
//});
//
//LibraryArtistView = Backbone.View.extend({
//    initialize: function() {
//        this.listenTo(this.model, 'change', this.render)
//    },
//
//    render: function(){
//        console.log(this.model);
//        this.$el.html(this.model.attributes.name);
//    }
//});
//
//var model = new ArtistModel({ id: 1 });
//model.fetch();
//
//$(document).ready(function() {
//    var artist = new LibraryArtistView({
//        el: $('.artist').first(),
//        model: model
//    });
//});
