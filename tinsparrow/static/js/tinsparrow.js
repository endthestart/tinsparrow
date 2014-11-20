var SONG_SELECTOR = '.js-song',
    PLAYER_SELECTOR = '#audio-player';

QueueView = Backbone.View.extend({
    el: '.js-queue-list',
    events: {
        "click .js-song": "playSong"
    },
    initialize: function () {
        this.$player = $(PLAYER_SELECTOR)
        this.$songs = this.$el.find(SONG_SELECTOR);
        this.audioPlayer = this.$player.get(0);
    },
    playSong: function () {
        var $song = $(event.target);

        this.$songs.removeClass('active');
        $song.addClass('active');

        this.$player.empty().append(
            '<source src="' + $song.data('url') + '" type="audio/mp4">'
        );

        this.audioPlayer.load()
        this.audioPlayer.play();
    }
});

qv = new QueueView();


