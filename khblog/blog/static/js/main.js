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

function getCookies() {
    var cookies = null;
    if (document.cookie && document.cookie !=='') {
        var cookie = document.cookie.split(';');
        console.log(cookie);
    }
}