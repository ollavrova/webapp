/*<![CDATA[*/
$(document).ready(function () {

    // plugin for close alert messages
       $('#myAlert').on('closed.bs.alert', function () {
            $('.alert').alert('close');
        });

    // add like function
    $('#like').click(function(){
      $.ajax({
               type: "POST",
               url: $(this).attr('action'),
               data: {
                   'slug': $(this).attr('name'),
                   'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
               },
               dataType: "json",
               contentType: "application/json; charset=utf-8",
               success: function(response) {
                   $('#result_like').html(
                       '<div class="alert alert-success messages" role="alert">'+
                       '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
                       '<span aria-hidden="true">&times;</span></button><p class="success">'+
                       response.message + '</p></div>');
                   $('#likes').text(response.likes_count+' likes');
                   $('#like').val(response.act);
                },
                error: function(rs, e) {
                    $('#result_like').text(e);
                       console.log(rs.responseText);
                }
          });
    });

    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
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
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
    });
/*]]>*/