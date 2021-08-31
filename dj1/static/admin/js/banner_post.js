$(function (){
    let $tag_select=$("#category-select");                  //分类选择
    let $news_select=$('#news-select');                     //文章选择
    let $priority_select=$('#priority');                    //优先级
    let $img_select=$('.banner-image');                     //图片选择按钮
    let $img_url=$("input[name='banner-image-select']");    //图片更换
    let $update=$('#save-btn');                             //保存按钮


    //图片上传
    $img_select.click(function (){
        $(this).prev().click()
    })
    $img_url.change(function (){
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

    //显示新闻列表
    $tag_select.change(function (){
        let tag_id=$(this).val();
        console.log(tag_id)
        if(tag_id==='0'){
            $news_select.children('option').remove();
            $news_select.append(`<option value="0">--请选择文章--</option>`);
            return
        }
        $.ajax({
            url: '/admin/news_select/'+tag_id+'/',
            type:'GET',
            dataType:'json'
        })
            .done(function (res){
                if(res.errno==='0'){
                    $news_select.children('option').remove();
                    $news_select.append(`<option value="0">--请选择文章--</option>`);
                    res.data.news.forEach(function (one_news) {
                        let content = `<option value="${one_news.id}">${one_news.title}</option>`;
                        $news_select.append(content)
                    });
                }else{
                    fAlert.alertErrorToast(res.errmsg)
                }
            })
            .fail(function (){
                message.showError(res.errmsg)
            })
    })

    //上传轮播图
    $update.click(function (){
        let image=$img_select.attr('src');
        let tag=$tag_select.val();
        let news=$news_select.val();
        let priority=$priority_select.val();

        if(image==='/static/images/banner_default.png'){
            message.showError('请选择图片')
            return
        }
        if(tag==='0'){
            message.showError('请选择文章分类')
            return
        }
        if(news==='0'){
            message.showError('请选择文章')
            return
        }
        if(priority==='0'){
            message.showError('请选择优先级')
            return
        }
        fAlert.alertConfirm({
            title:'请确认添加轮播图？',
            confirmText: "确认",
            confirmCallback:function (){
                let data={
                    'image':image,
                    'tag':tag,
                    'news':news,
                    'priority':priority
                }
                $.ajax({
                    url:'/admin/admin_banner_post/',
                    data: JSON.stringify(data),
                    dataType: 'json',
                    type: 'POST',
                    contentType: "application/json; charset=utf-8",
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            message.showSuccess(res.errmsg)
                            setTimeout(function (){
                                window.location.href='/admin/admin_banner'
                            },1000)
                        }else {
                            message.showError(res.errmsg)
                        }
                    })
                    .fail(function (){
                        message.showError('服务器超时请重试')
                    })
            }
        })

    })


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