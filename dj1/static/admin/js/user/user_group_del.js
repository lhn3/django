

$(function (){
    let $del=$('.btn-del');       //删除按钮

    //删除
    $del.click(function (){
        let i =this;
        let group_id=$(this).parents('tr').data('id');
        let Title=$(this).parents('tr').data('name');
        fAlert.alertConfirm({
            title:'确定删除'+'【'+Title+'】'+'吗？',
            confirmText:'确定',
            type:'error',
            confirmCallback:function (){
                $.ajax({
                    url:'/admin/admin_usergroup_del/'+group_id+'/',
                    type: 'DELETE',
                    dataType:'json',
                })
                    .done(function (res){
                        if (res.errno){
                            message.showSuccess(res.errmsg)
                            $(i).parents('tr').remove()
                        }else {
                            message.showError(res.errmsg)
                        }
                    })
                    .fail(function (){
                        message.showError('服务器超时，请重试！')
                    })
            }
        })
    })





// get cookie using jQuery
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Setting the token on the AJAX request
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

})