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
}

function postToVk(post_id, uid) {
        $.ajax(
            {
                url: '/api/postToVk?post_id=' + post_id + '&uid=' + uid,
                type: 'GET'
            }
        );
}