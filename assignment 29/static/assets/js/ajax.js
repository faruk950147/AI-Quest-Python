$(document).ready(function () {
  $("#showHide").on("click", function(e){
    e.preventDefault()
    $("#icon").toggleClass("fa-eye")
  
    if($("#id_password, #id_password2, #id_current_password").attr("type") === "password"){
      $("#id_password, #id_password2, #id_current_password").attr("type", "text")
    }
    else{
      $("#id_password, #id_password2, #id_current_password").attr("type", "password")
    }
});
});
// main.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    headers: { "X-CSRFToken": csrftoken }
});
