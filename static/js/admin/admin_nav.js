$(function(){
    var pathname = window.location.pathname;
    console.log(pathname);
    if(pathname.endsWith("")) {
        $("#index").addClass("active");
    }
    if(pathname.endsWith("video_list/")) {
        $("#video_list").addClass("active");
    }
    if(pathname.indexOf("video_edit/") >= 0){
        $("#video_list").addClass("active");
    }
    if(pathname.endsWith("/video_add/")) {
        $("#video_add").addClass("active");
    }
    if(pathname.endsWith("classification_list/")) {
        $("#classification_list").addClass("active");
    }
    if(pathname.indexOf("classification_edit/") >= 0){
        $("#classification_list").addClass("active");
    }
    if(pathname.endsWith("classification_add/")) {
        $("#classification_add").addClass("active");
    }
    if(pathname.endsWith("user_list/")) {
        $("#user_list").addClass("active");
    }
    if(pathname.indexOf("user_edit/") >= 0){
        $("#user_list").addClass("active");
    }
    if(pathname.endsWith("/user_add/")) {
        $("#user_add").addClass("active");
    }
    if(pathname.endsWith("/comment_list/")) {
        $("#comment_list").addClass("active");
    }
    if(pathname.indexOf("/setting/") >= 0) {
        $("#setting").addClass("active");
    }
    if(pathname.indexOf("/subscribe/") >= 0){
        $("#subscribe").addClass("active");
    }
    if(pathname.indexOf("/feedback_list/") >= 0){
        $("#feedback_list").addClass("active");
    }
});