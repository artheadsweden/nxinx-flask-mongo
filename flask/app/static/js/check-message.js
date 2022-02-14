setInterval(checkMsg, 10000);

function checkMsg() {

    fetch('http://localhost/ajax/check_msg')
        .then(response => response.json())
        .then(respObj => {
            let msgSymbol = document.getElementById("message-symbol");
            let msgCount = document.getElementById("message-count");
            if(respObj.unread_msg_count > 0) {
                msgSymbol.classList.remove("no-new-msg");
                msgSymbol.classList.add("new-msg");
                msgSymbol.classList.remove("fa-envelope-open");
                msgSymbol.classList.add("fa-envelope");
                msgCount.innerHTML = respObj.unread_msg_count;
            }
            else {
                msgSymbol.classList.remove("new-msg");
                msgSymbol.classList.add("no-new-msg");
                msgSymbol.classList.remove("fa-envelope");
                msgSymbol.classList.add("fa-envelope-open");
                msgCount.innerHTML = "";
            }
        })
}