$(function () {
    $('.vote-btn').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/forum/up/' + $('#id').html() + '/' + $('#title').html,
            type: 'post',
            dataType: 'json',
            cache: false,
            data: {},
            success: function (data) {
                if (data.res === 1) {
                    if (data.up === 'true') {
                        $('.vote-btn').html('Voted');
                        $('.vote-btn').addClass('voted');
                        $('.vote-btn').removeClass('unvoted');
                        var count = parseInt($('#up_count').html()) + 1;
                        $('#up_count').html(count)
                    } else {
                        $('.vote-btn').html('Up');
                        $('.vote-btn').addClass('unvoted');
                        $('.vote-btn').removeClass('voted');
                        var count = parseInt($('#up_count').html()) - 1;
                        $('#up_count').html(count)
                    }
                }

            }
        })
    })
});


