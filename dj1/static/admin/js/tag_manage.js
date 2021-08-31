$(function (){
    //添加
    let $add=$('#btn-add-tag'); //获取按钮
        $add.click(function (){     //点击add事件
        fAlert.alertOneInput({ //自定义弹窗事件
            title:'请输入标签',
            text:'长度限制在20个字',
            placeholder:'请输入文章标签',
            confirmCallback:function confirmCallback(inp){
                let Data={
                    'title':inp
                };
                $.ajax({
                    url:'/admin/admin_tags/',
                    type:'POST',
                    data:JSON.stringify(Data),
                    contentType:'application/json;charset=utf-8',
                    dataType:'json'
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            fAlert.alertSuccessToast(res.errmsg)
                            setTimeout(function (){
                                window.location.reload();
                            },1000)
                        }else {
                            swal.showInputError(res.errmsg);
                        }
                    })
                    .fail(function (){
                        message.showError('服务器超时，请重试')
                    })
            }
        })
    })




    //编辑
    let $edit=$('.btn-edit');
        $edit.click(function (){     //点击事件
            let tag_id=$(this).data('id');
            let tag_name=$(this).parents('tr').data('name')
        fAlert.alertOneInput({ //自定义弹窗事件
            title:'正在编辑'+'【'+tag_name+'】',
            text:'长度限制在20个字',
            placeholder:'请输入新标签名称',
            confirmCallback:function confirmCallback(inp){
                let Data={
                    'title':inp
                };
                $.ajax({
                    url:'/admin/admin_retag/'+tag_id+'/',
                    type:'PUT',
                    data:JSON.stringify(Data),
                    contentType:'application/json;charset=utf-8',
                    dataType:'json'
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            fAlert.alertSuccessToast(res.errmsg)
                            setTimeout(function (){
                                window.location.reload();
                            },1000)
                        }else {
                            swal.showInputError(res.errmsg);
                        }
                    })
                    .fail(function (){
                        message.showError('服务器超时，请重试')
                    })
            }
        })
    })



    //删除
    let $del=$('.btn-del');
        $del.click(function (){     //点击事件
            let tag_id=$(this).data('id');
            let tag_name=$(this).parents('tr').data('name')
        fAlert.alertConfirm({ //自定义弹窗事件
            title:'确定删除'+'【'+tag_name+'】'+'标签吗？',
            type:'error',
            confirmButtonText:'确定',
            cancelButtonText:'取消',
            confirmCallback:function confirmCallback(){
                $.ajax({
                    url:'/admin/admin_deltag/'+tag_id+'/',
                    type:'POST',
                    dataType:'json'
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            fAlert.alertSuccessToast(res.errmsg)
                            setTimeout(function (){
                                window.location.reload();
                            },500)
                        }else {
                            swal.showInputError(res.errmsg);
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

