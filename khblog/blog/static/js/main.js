function getRequest() {
    var search = document.getElementById('text-input').value;
    var html = $.ajax({
        url: '/',
        type: 'GET',
        data: {Search: search},
        async: false,
        success: function (data) {
            $('#posts').replaceWith($('#posts', data));
        }
    });
    return false;
}

function postToVk(post_id) {
    fetch(
        "/api/postToVk?post_id=" + post_id,
        {method: "GET"}
    );
}

function postLike(pk) {
    var csrf = document.cookie.split('=')[1];
    var html = $.ajax({
        url: "/api/post/like/", type: 'POST',
        data: {csrfmiddlewaretoken: csrf, pk: pk},
        success: function(data){
                $('#likes').text(data.likes);
                $('#dislikes').text(data.dislikes);}
        }
    );
}

function postDislike(pk){
    var csrf = document.cookie.split('=')[1];
    var html = $.ajax({
        url: "/api/post/dislike/", type: 'POST',
        data: {csrfmiddlewaretoken: csrf, pk: pk},
        success: function(data){
                $('#likes').text(data.likes);
                $('#dislikes').text(data.dislikes);}
        }
    );
}

