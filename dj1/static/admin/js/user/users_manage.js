$(function (){
    let $btn=$('#btn-edit-user');                                   //更新按钮
    let $del=$('.btn-del');                                         //删除按钮
    let staff_old=$("input[name='login_admin']:checked").val();     //旧_是否能登录后台
    let superuser_old=$("input[name='is_superuser']:checked").val();//旧_是否是超级管理员
    let active_old=$("input[name='is_active']:checked").val();      //旧_是否激活
    let group_old=$("#add_group").val();                            //旧_分组


    //删除
    $del.click(function (){
        let i=this
        let user_id=$(this).parents('tr').data('id');
        let user_name=$(this).parents('tr').data('name');
        fAlert.alertConfirm({
            type: 'error',
            title: '确定删除'+'【'+user_name+'】用户？',
            confirmText: '确定',
            cancelText: '取消',
            confirmCallback:function (){
                $.ajax({
                    url:'/admin/admin_users_del/'+user_id+'/',
                    dataType: 'json',
                    type:'DELETE',
                })
                    .done(function (res){
                        if(res.errno==='0'){
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



//编辑
    $btn.click(function (){
        let i=this;
        let user_id=$(i).data('user-id');
        let username=$(i).data('user-name');
        let staff=$("input[name='login_admin']:checked").val();     //新_是否能登录后台
        let superuser=$("input[name='is_superuser']:checked").val();//新_是否是超级管理员
        let active=$("input[name='is_active']:checked").val();      //新_是否激活
        let group=$("#add_group").val();                            //新_分组

        if (staff_old===staff && superuser_old===superuser && active_old===active && JSON.stringify(group_old)===JSON.stringify(group)){
            message.showError('未作修改，无需更新！')
            return
        }
        fAlert.alertConfirm({
            title:'请确定更新'+'【'+username+'】用户权限？',
            confirmText:'确定',
            cancelText:'取消',
            confirmCallback:function (){
                let data={
                    'is_staff':staff,
                    'is_superuser':superuser,
                    'is_active':active,
                    'groups':group
                }
                $.ajax({
                    url:'/admin/admin_users_put/'+user_id+'/',
                    dataType:'json',
                    data:JSON.stringify(data),
                    contentType:'application/json:charset=utf-8',
                    type:'PUT'
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            message.showSuccess(res.errmsg)
                            setTimeout(function (){
                                window.location.href='/admin/admin_users';
                            },1500)
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