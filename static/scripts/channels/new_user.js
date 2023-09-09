
       /* var socket = new ReconnectingWebSocket(url, null, {debug: true, reconnectInterval: 3000});

         //OR

        var socket = new ReconnectingWebSocket(url);
        socket.debug = true;
        socket.timeoutInterval = 5400; */


        endpoint = 'ws: //127.0.0.1: 8000 / new-user /' // 1

        var socket = new ReconnectingWebSocket (endpoint) // 2

        // ...
        socket.onmessage = function (e) {
          console.log ("message", e)
          var userData = JSON.parse (e.data)
          console.log ('userData.html_users')
          console.log (userData.html_users)
          //$('#new_user').html (userData.html_users)
        }
        // ....


        /*const roomName = JSON.parse(document.getElementById('room-name').textContent);

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').value += (data.message + '\n');
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
         */