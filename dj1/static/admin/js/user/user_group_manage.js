

$(function (){
    let $edit=$('#btn-pub-news');       //更新按钮
    let group_id=$edit.data('news-id');//用户ID

    //编辑
    $edit.click(function (){
        let Title=$('#news-title').val();       //组名
        let power=$('#group-permissions').val();//权限
        console.log(power)
        if(!Title){
            message.showError('请输入组名！')
            return
        }
        if(power['length']===0){
            message.showError('至少选择一项权限！')
            return
        }
        let url=group_id?'/admin/admin_usergroup_put/'+group_id+'/':'/admin/admin_usergroup_post/';
        fAlert.alertConfirm({
            title:'确定更新'+'【'+Title+'】'+'组信息？',
            confirmText:'确定',
            confirmCallback:function (){
                let Data={
                    'name':Title,
                    'permissions':power
                }
                $.ajax({
                    url:url,
                    data:JSON.stringify(Data),
                    dataType:'json',
                    contentType:'application/json; charset=utf-8',
                    type:group_id?'PUT':'POST',
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            message.showSuccess(res.errmsg)
                            setTimeout(function (){
                                window.location.href='/admin/admin_usergroup/'
                            },1500)
                        }else {
                            message.showError(res.errmsg)
                        }
                    })
                    .fail(function (){
                        message.showError('服务器超时，请重试')
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