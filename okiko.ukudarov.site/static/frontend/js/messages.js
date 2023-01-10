$(function () {
    "use strict";
    $('.chat__message__dt ').on('click', function () {
        $('.group_messages .chat__message__dt.active').removeClass('active');
        $(this).addClass('active');
        var gid = $(this).attr('data-gid')
        var img = $(this).find("img").attr('src');
        var title = $(this).find(".user-status-title span").html();

        $('#select-user-img').attr('src', img);
        $('#select-user-title').html(title);
        $("#chat-area").html("");
        getNewChatData(gid);

    });

    setInterval(() => {
        getMessage()
    }, 3000);

});
// Get the input field
var input = document.getElementById("chat-box");

// Execute a function when the user releases a key on the keyboard
if (input) {

    input.addEventListener("keyup", function (event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            sendMessage()
        }
    });
}

function sendMessage() {
    var msg = $('#chat-box').val()
    if (!msg) {
        alert("Please enter a message");
    }
    var fd = new FormData();
    var uri = $('#send-uri').val();
    fd.append('group_id', $('#gid').val())
    fd.append('msg', msg)
    fd.append('sender_id', $('#user-type').val())
    $.ajax({
        url: uri,
        data: fd,
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function (data, textStatus, jqXHR) {

            $('#chat-box').val("");
            getMessage()

        }
    });
}

function getMessage() {

    if ($("#getmsguri").val()) {

        var formData = {
            lastmsg: $("#lastmsg").val(),
            gid: $("#gid").val(),
            guard: $('#user-type').val()
        };
        $.ajax({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },
            url: $("#getmsguri").val(),
            type: "POST",
            data: formData,
            async: false,
            success: function (response, textStatus, jqXHR) {

                $("#chat-area").append(response.data);

                $("#chat-area").animate({
                    scrollTop: $('#chat-area').prop("scrollHeight")
                }, 1000);

                $("#lastmsg").val(response.lastmsgid)
            },
            error: function (jqXHR, textStatus, errorThrown) {

            }
        });
    }

}

function getNewChatData(gid) {
    $('#gid').val(gid)
    $("#lastmsg").val(0)
    getMessage()
}
