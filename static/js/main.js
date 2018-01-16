
// write js code here
(function (){
$(".user-item").on('click', function(event){
$(this).addClass("active-user");
$(this).siblings().removeClass( "active-user");
toggleViews();
readMessages($(this));

});

function toggleViews(){
    $(".chat-main").removeClass("hidden");
    $(".chat-info").addClass("hidden");
}

function readMessages(element){

    element.find(".username").removeClass('unread-active');
    element.find(".unread-notify").remove();
}

}());