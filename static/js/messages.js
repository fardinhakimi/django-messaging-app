
// write js code here

(function (){
    
    const messageList = $("#message-list");
    const messageBox = $(".conversation");

    function makeApiCall (url, method, data){

    return new Promise( function(resolve, reject) {

     $.ajaxSetup({
        beforeSend: function(xhr, settings){
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

        $.ajax({
            url: url,
            method: method,
            data: data,
            dataType: "json"
          }).done(function( data ) {
              resolve(data);
          }).fail(function(err) {
              reject(err);
          });
    });
}

$(".user-item").on("click", function(){
    let data = {
        'user_id': $(this).attr('id')
    };
    renderConversation(data);
    setActiveUser($(this).attr("id"));
    scrollToBottom();
});

$("#message-form").on("submit", function(event){
    event.preventDefault();
    postMessage( 
        {
            "recipient_id": $(".all-users").find(".active-user").attr('id'),
            "conversation_id":  $(".conversation").attr("id"),
            "message":  $("#message").val()
        }
    );
    $("#message").val("");
    scrollToBottom();
});


function postMessage(sendData){

    let promise = makeApiCall('/post-message/', 'POST', sendData);

    promise.then(function(data){
        let user = data.members.sender;
        let messageItem = renderMessage(data.message, user, 
            {'messageDirection':'message-sender',
            'usernameDirection': 'username-sender'
        });
        messageList.append(messageItem);
    }).catch(function(err){
        alert("failed to send message!");
    });
}


    function renderConversation(sendData){
   
        var promise = makeApiCall('/get-messages', 'GET', sendData);

        promise.then(function(data){


            $(".conversation").attr("id",data.conversation_id);

            let messages = JSON.parse(data.messages);
            messageList.empty();

            if (messages.length>0){

                for (let i=0; i<messages.length; i++){
                    messageItem = renderMessageItem(messages[i], data.members);
                    messageList.append(messageItem);
                }
            }
            return true;
        })
        .catch(function(err){
            console.log(err);
            messageList.append(renderErrorMessage());
            return false;
        });
        }


        function renderMessageItem(messageData, members){

            let message = messageData.fields.value,
                senderId = members.sender.id,
                ownerId = messageData.fields.owner,
                sender = members.sender,
                recipient = members.recipient;

            if (senderId == ownerId){
                messageItem= renderMessage(message, sender, 
                    {'messageDirection':'message-sender',
                    'usernameDirection': 'username-sender'
                });
            }else{
                messageItem = renderMessage(message, recipient,
                     {'messageDirection':'message-recipient',
                     'usernameDirection': 'username-recipient'
                    }
        );
            }
            return messageItem;
        }

        function renderMessage(message, user, directionClass){
            return `
            <li> 
            <span class='message-box ${directionClass.messageDirection}'>
            ${message}
            </span>
            </li>`;
        }

        function renderErrorMessage(){
            return `<div class ='error-messages'>
             <p>Something went wrong. Please refresh the page!
             </p></div>
            `;
        }

function scrollToBottom(){
      messageBox.stop().animate({
           scrollTop: messageBox[0].scrollHeight
        }, 1000);
}


function setActiveUser(active_id){
    localStorage.setItem("activeUser", active_id);
} 

// render conversation with active user after page reload
    if(localStorage.getItem("activeUser")) {
        $(".all-users").find("#"+localStorage.getItem("activeUser")).trigger("click", function(){
            renderConversation(localStorage.getItem("activeUser"));
        });
    }

//  csrf and cookies 
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
    // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method){
 // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

}());


