
// write js code here
(function (){
$(".user-item").on('click', function(event){
$(this).addClass("active-user");
$(this).siblings().removeClass( "active-user");
toggleViews();
readMessages();

});

function toggleViews(){
    $(".chat-main").removeClass("hidden");
    $(".chat-info").addClass("hidden");
}

function readMessages(){
    $("#username").removeClass('unread-active');
    $(".unread-notify").remove();
}

}());