

$(function (){
    let $img_select=$("#upload-image-server");  //图片上传按钮
    let $img_url=$('#news-thumbnail-url');      //图片URL
    let $file_select=$('#upload-file-server');  //文件上传按钮
    let $file_url=$("#docs-file-url");          //文件URL
    let $docs_put=$('#btn-pub-news');           //更新按钮
    let $del=$(".btn-del");                     //删除按钮

    //获取页面原本数据
    let title_old=$('#news-title').val();
    let img_old=$img_url.val();
    let desc_old=$('#news-desc').val();
    let file_old=$file_url.val();
    //上传图片
    $img_select.change(function (){
        let image=this.files[0];
        let ImageData=new FormData();
        ImageData.append('image_files',image);
        $.ajax({
            url:'/admin/news/img_dfs/',
            dataType:'json',
            method:'POST',
            data:ImageData,
            contentType:false,
            processData:false
        })
            .done(function (res){
                if (res.errno==='0'){
                    message.showSuccess(res.errmsg)
                    let img_url=res['data']['image_url']
                    $img_url.val(img_url)
                }else{
                    message.showError(res.errmsg)
                }
            })
            .fail(function (){
                message.showError('服务器超时，请重试!')
            })
    })

    //上传文件
    $file_select.change(function (){
        let text=this.files[0];
        let FileData=new FormData();
        FileData.append('text_file',text);
        $.ajax({
            url:'/admin/news/img_dfs/',
            dataType:'json',
            method:'POST',
            data:FileData,
            processData:false,
            contentType:false,
        })
            .done(function (res){
                if (res.errno==='0'){
                    message.showSuccess(res.errmsg)
                    let file_url=res['data']['text_url']
                    $file_url.val(file_url)
                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function (){
                message.showError('服务器超时，请重试！')
            })
    })

    //更新or上传
    $docs_put.click(function (){
        let doc_id=$(this).data('news-id');
        let title=$('#news-title').val();
        let img=$img_url.val();
        let desc=$('#news-desc').val();
        let file=$file_url.val();


        if (!title){
            message.showError('请填写文档标题！')
            return
        }
        if (!img){
            message.showError('请上传文档图片！')
            return
        }
        if (!desc){
            message.showError('请填写文档描述！')
            return
        }if (!file){
            message.showError('请上传文档！')
            return
        }
        if(title===title_old && img===img_old && desc===desc_old && file===file_old){
            message.showError('内容未更改，无需更新！')
            return
        }
        fAlert.alertConfirm({
            title:doc_id?'确定更新文档？':'确定发布文档？',
            confirmText: "确认",
            confirmCallback:function (){
                let url=doc_id?'/admin/admin_docs_put/'+doc_id+'/':'/admin/admin_docs_post/';
                let Data={
                    'title':title,
                    'file_url':file,
                    'image_url':img,
                    'desc':desc
                }
                $.ajax({
                    url:url,
                    data:JSON.stringify(Data),
                    type:doc_id?'PUT':'POST',
                    dataType:'json',
                    contentType:'application/json;charset=utf-8'

                })
                    .done(function (res){
                        if (res.errno==='0'){
                            fAlert.alertSuccessToast(res.errmsg)
                            setTimeout(function (){
                                window.location.href='/admin/admin_docs/'
                            },1000)
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

    //删除
    $del.click(function (){
        let i=this;
        let doc_id=$(this).parents('tr').data('id');
        let title=$(this).parents('tr').data('name');
        fAlert.alertConfirm({
            title:'请确认删除'+'【'+title+'】',
            type:'error',
            confirmText: "确认",
            cancelText: "取消",
            confirmCallback:function (){
                $.ajax({
                    url:'/admin/admin_docs_del/'+doc_id+'/',
                    type:'DELETE',
                    dataType:'json',
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            message.showSuccess(res.errmsg)
                            $(i).parents('tr').remove();
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