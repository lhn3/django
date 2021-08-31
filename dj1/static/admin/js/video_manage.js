$(function (){
    let $img_select=$('#upload-image-server');  //选择图片按钮
    let $img_url=$('#news-thumbnail-url');      //图片地址显示
    let $video_select=$('#upload-file-server'); //视频选择
    let $video_url=$('#docs-file-url');         //视频地址
    let $pub=$('#btn-pub-news');                //更新发布按钮


    //图片上传dfs
    $img_select.change(function (){
        let i=this
        let img=this.files[0];
        let Data=new FormData();
        Data.append('image_files',img)
        $.ajax({
            url:'/admin/news/img_dfs/',
            data:Data,
            dataType:'json',
            method:'POST',
            processData:false,
            contentType:false
        })
             .done(function (res) {
                 if (res.errno === "0") {
                     message.showSuccess("图片上传成功");
                     let ImageUrl = res.data.image_url;
                     // let $inpuUrl = $(i).parents('.input-group').find('input:nth-child(1)');
                     $img_url.val(ImageUrl);
                     } else {
                     message.showError(res.errmsg)
                 }
             })
            .fail(function () {
                message.showError('服务器超时，请重试！');
            });
    })




    //视频上传
    let sdk=baidubce.sdk;
    let vod_client=sdk.VodClient;
    let config={
        endpoint:'http://vod.bj.baidubce.com',
        credentials:{
            ak:'aee47a29e8c345189b1f25f61590a724',
            sk:'b30e195099694c7bac90518924849bcc',
        }
    };
    let client=new vod_client(config);

    $video_select.change(function (){
        let Title=$('#news-title').val();
        let Profile=$('#news-desc').val();
        let img=$img_url.val();
        console.log(img)
        if(!Title){
            message.showError('请输入标题后再上传视频文件！')
            return
        }
        if(!Profile){
            message.showError('请输入课程简介后再上传视频文件！')
            return
        }
        if(!img){
            message.showError('请选择课程封面后再上传视频文件！')
            return
        }

        let video=this.files[0];
        let video_type=video.type;              //获取文件格式
        let data=new Blob([video],{type:video_type});  //一个对象
        let title='十里';
        let des='这是一个视频';
        client.createMediaResource(title,des,data)
            .then(function (response){               //上传成功
                let bs=response.body.mediaId;
                let res='http://me7tbcb2hrmacnc0gsw.exp.bcevod.com/'+bs+'/'+bs+'.m3u8';
                $video_url.val(res)
                message.showSuccess('视频上传成功')
            })
            .catch(function (error){
                console.log(error);
                message.showError('视频上传失败，请重试！')
                client.on('progress',function (evt){        //监听
                    console.log(evt)
                });
            });
    });



    //更新or上传
    $pub.click(function (){
        let Title=$('#news-title').val();           //标题
        let profile=$('#news-desc').val();          //课程简介
        let img_url=$img_url.val();                 //图片
        let video_url=$video_url.val();             //视频

        let outline=$('.markdown-body').html()       //课程大纲
        // let outline = window.editor.txt.html();
        // let outline = window.editor.txt.text();

        let teacher=$('#course-teacher').val();     //讲师
        let category=$('#course-category').val();   //f分类
        if(!Title){
            message.showError('请输入标题！')
            return
        }
        if(!profile){
            message.showError('请输入课程简介！')
            return
        }
        if(!img_url){
            message.showError('请上传课程封面图片！')
            return
        }
        if(!video_url){
            message.showError('请上传课程视频文件！')
            return
        }
        if(!outline || outline==='<p><br></p>'){
            message.showError('请输入课程大纲！')
            return
        }
        if(!teacher || teacher==='0'){
            message.showError('请选择课程讲师！')
            return
        }
        if(!category || category==='0'){
            message.showError('请选择课程分类！')
            return
        }

        let v_id=$(this).data('news-id');
        fAlert.alertConfirm({
            title:v_id?'确定更新课程？':'确定发布课程？',
            confirmText:'确定',
            confirmCallback:function (){
                let url=v_id?'/admin/admin_video_put/'+v_id+'/':'/admin/admin_video_post/';
                let Data={
                    'title':Title,
                    'cover_url':img_url,
                    'video_url':video_url,
                    'profile':profile,
                    'outline':outline,
                    'teacher':teacher,
                    'category':category,
                }
                $.ajax({
                    url:url,
                    data:JSON.stringify(Data),
                    dataType: 'json',
                    contentType: 'application/json;charset=utf-8',
                    type: v_id?'PUT':'POST'
                })
                    .done(function (res){
                        if(res.errno==='0'){
                            fAlert.alertSuccessToast(res.errmsg)
                            setTimeout(function (){
                                window.location.href='/admin/admin_video/';
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