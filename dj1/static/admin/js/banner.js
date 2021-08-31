$(function (){
    let $del=$('.close-btn');    //删除
    let $edit=$('.update-btn');  //保存
    let $img=$(".banner-image"); //图片
    let $img_input=$('input[name=banner-image-select]');  // image input元素

    //删除
    $del.click(function (){
        let i=this;
        let banner_id=$(this).parents('li').data('banner-id');
        fAlert.alertConfirm({
            title:'是否删除此轮播图',
            type:'error',
            confirmText: "确认",
            confirmCallback:function (){
                $.ajax({
                    url:'/admin/admin_banner_del/'+banner_id+'/',
                    dataType:'json',
                    type:'DELETE'
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            message.showSuccess(res.errmsg)
                            $(i).parents('li').remove();
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


    //图片更换dfs
    $img.click(function (){
        $(this).prev().click();
    });
    $img_input.change(function (){
        let i=this;
        let file=this.files[0];
        let Data=new FormData();
        Data.append('image_files',file);
                $.ajax({
            url:'/admin/news/img_dfs/',
            method:'POST',
            data:Data,
            processData:false,
            contentType:false
        })
            .done(function (res){
                if(res.errno==='0'){
                    message.showSuccess(res.errmsg);
                    let url=res['data']['image_url']
                    $(i).next().attr('src',url)     //只更换点击的这个轮播图的图片
                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function (){
                message.showError('服务器超时请重试')
            })
    })


    //编辑轮播图
    $edit.click(function (){
        let img_url=$(this).parents('li').find('.banner-image').attr('src');//获取图片路由
        let priority=$(this).parents('li').find('#priority').val();         //获取优先级
        let banner_id=$(this).parents('li').data('banner-id');              //获取id

        let old_img_url=$(this).data('image-url');
        let old_priority=$(this).data('priority');

        if (priority==='0'){
            message.showError('请选择优先级');
            return
        }
        if (!img_url){
            message.showError('请选择封面');
            return
        }
        if(priority==old_priority && img_url==old_img_url){
            message.showError('未作修改无需更新');
            return
        }
        fAlert.alertConfirm({
             title:'确认更新此轮播图？',
            confirmText: "确认",
            confirmCallback:function (){
                 let data={
            'img_url':img_url,
            'priority':priority,
        };
        $.ajax({
            url:'/admin/admin_banner_put/'+banner_id+'/',
            data:JSON.stringify(data),
            type:'PUT',
            dataType: 'json',
            contentType: 'application/json;charset=utf-8',
        })
            .done(function (res){
                if(res.errno==='0'){
                    message.showSuccess(res.errmsg)
                    setTimeout(function (){
                        window.location.href='/admin/admin_banner/'
                    },1000)
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