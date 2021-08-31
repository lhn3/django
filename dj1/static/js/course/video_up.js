$(function () {
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
    let $file=$('.up');
    $file.change(function (){
        let video=this.files[0];
        let video_type=video.type;              //获取文件格式
        let data=new Blob([video],{type:video_type});  //一个对象
        let title='十里';
        let des='这是一个视频';
        client.createMediaResource(title,des,data)
            .then(function (response){               //上传完成
                let bs=response.body.mediaId;
                let res='http://me7tbcb2hrmacnc0gsw.exp.bcevod.com/'+bs+'/'+bs+'.m3u8';
                console.log(res);
            })
            .catch(function (error){
                console.log(error);
                client.on('progress',function (evt){        //监听
                    console.log(evt)
                });
            });
    });
});