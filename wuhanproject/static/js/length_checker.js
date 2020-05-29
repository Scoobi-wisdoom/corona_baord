$(function () {
    $('textarea.content').keyup(function () {
        bytesHandler(this);
    });
});

function getTextLength(str) {
    var len = 0;

    for (var i = 0; i < str.length; i++) {
        if (escape(str.charAt(i)).length == 6) {
            len++;
        }
        len++;
    }
    return len;
}

function bytesHandler(obj) {
    var text = $(obj).val();
    var length = getTextLength(text);
    if (length > 5000) {
        alert("max length is 5000")

        $('textarea.content').val($('textarea.content').val().substring(0, 5000));

    }
}