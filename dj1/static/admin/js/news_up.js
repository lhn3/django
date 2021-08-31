

$(function (){
    //图片上传到dfs
    let $up_server=$('#upload-news-thumbnail');
    let $image_url=$('#news-thumbnail-url');

    $up_server.change(function (){
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
                    $image_url.val(url);
                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function (){
                message.showError('服务器超时请重试')
            })
    })



//文章更新--------------文章上传------------------------------------
    let $news_up=$('#btn-pub-news');
    $news_up.click(function (){
        let title=$('#news-title').val();
        let desc = $("#news-desc").val();
        let tag=$('#news-category').val();
        let img_url=$image_url.val();
        let content=$('.markdown-body').html();
        let news_id=$(this).data('news-id')
        if (!title){
            message.showError('请填写文章标题')
            return
        }
        if (!desc){
            message.showError('请填写文章摘要')
            return
        }
        if (!tag){
            message.showError('请选择文章标签')
            return
        }
        if (!img_url){
            message.showError('请上传文章图片缩略图')
            return
        }
        if (!content||content==='<p><br></p>'){
            message.showError('请输入文章内容')
            return
        }
        //有news_id走前面的url，没有则走后面url
        let url=news_id?'/admin/admin_news_put/'+news_id+'/':'/admin/admin_news_post/'
        let data={
            'title':title,
            'digest':desc,
            'tag':tag,
            'image_url':img_url,
            'content':content,
        }
        // console.log(data)
            $.ajax({
                url:url,
                data:JSON.stringify(data),
                type:news_id?'PUT':'POST',
                contentType: 'application/json;charset=utf-8',
                dataType:'json',
            })
                .done(function (res){
                    if (res.errno==='0'){
                        message.showSuccess(res.errmg)
                        setTimeout(function (){
                            window.location.href='/admin/admin_news/';
                        },1500)
                    }else {
                        fAlert.alertErrorToast(res.errmsg)
                    }
                })
                .fail(function (){
                    message.showError('服务器超时，请重试！')
                })
    })



 // get cookie using jQuery---------------------------------------
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