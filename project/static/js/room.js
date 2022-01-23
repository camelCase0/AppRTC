var socket;
    $(document).ready(function(){
        socket = io.connect('http://' + document.domain + ':' + location.port + '/room');
        socket.on('connect', function() {
            socket.emit('join', {});
        });
        socket.on('status', function(data) {
            $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });
        socket.on('message', function(data) {
            $('#chat').val($('#chat').val() + data.msg + '\n');
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });
        $('#send').click(function(e) {
                text = $('#text').val();
                $('#text').val('');
                socket.emit('text', {msg: text});
        });
    });
    function leave_room() {
        socket.emit('left', {}, function() {
            socket.disconnect();
            // go back to the login page
            window.location.href = "{{ url_for('index') }}";
        });
    }

function switchCam()
    {
        if($('.cam').is(":checked"))
            $(".video").show();
        else
            $(".video").hide();
    }