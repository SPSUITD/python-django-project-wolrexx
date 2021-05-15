function WebsocketInit(name, username) {
    msg_area = document.getElementById('message-area');
    msg_area.focus();
    messages_area = document.querySelector('#messages');
    window.scrollTo(100, messages_area.scrollHeight);

    const chatSocket = new WebSocket('ws://' + window.location.host + `/ws/chat/${name}/`);

    chatSocket.onmessage = function(e) {
        console.log(e.data)
        data = JSON.parse(e.data)
        if (data.type == "message") {
            m = data.user == username ? "me" : "user";
            ph = data.user == username ? "right" : "left";
            messages_area.innerHTML += `<li class="${m}"><div class="message"><div class="entete"><h2>${data.user} </h2><h1>${data.date}</h1></div><span>${data.text}</span></div><img class="user-photo" align="${ph}" src="${data.photo}"></li>`;
            window.scrollTo(0, messages_area.scrollHeight);
        }
    }

    msg_area.onkeyup = function(e) {
        if (e.keyCode === 13) document.getElementById('send-message').click();
    }

    document.getElementById('send-message').onclick = function(e) {
        chatSocket.send(JSON.stringify({
            'type': "send_message", 'message': msg_area.value
        }));
        msg_area.value = '';

    };
};
