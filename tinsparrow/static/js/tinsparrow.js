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
    app.queue.currentSong = null;
    app.queue.push({'id': songID});
    app.queue.save();
}

function playSongNext(songID) {
    var song = app.queue.get({'id': app.queue.currentSong});
    console.log(song);
    var nextLocation = app.queue.indexOf(song)+1;
    console.log(nextLocation);
    app.queue.add({'id': songID}, {'at': nextLocation});
    app.queue.save();
}

function playSongLast(songID) {
    console.log(songID);
    app.queue.push({'id': songID});
    app.queue.save();
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

$('.play-queue').bind('click', function () {
    app.queue.playQueue();
});

$('.previous-queue').bind('click', function () {
    app.queue.playPreviousSong();
});

$('.next-queue').bind('click', function () {
    app.queue.playNextSong();
});
