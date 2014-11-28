var app = (function ($) {
    var config = $('#config');
    var app = JSON.parse(config.text());

    $(document).ready(function() {
        var router = new app.router();
    });

    return app;
})(jQuery);

function playSongNow(songID) {
    app.queue.reset();
    app.queue.push({'id': songID});
    app.queue.save();
    app.queue.playQueue();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

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

