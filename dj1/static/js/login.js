$(function (){
    let $login=$('.form-contain');
    $login.submit(function (e){
        e.preventDefault();
        let user_mobile=$('input[name=telephone]').val();
        if (user_mobile===''){
            message.showError('手机号码/用户名不能为空');
            return
        }
        if (!(/[\u4e00-\u9fa5\w\d]{3,11}/).test(user_mobile)){
            message.showError('手机号/用户名格式错误');
            return
        }
        let password=$('input[name=password]').val();
        if (password===''){
            message.showError('密码不能为空');
            return
        }
        let status=$('input[type=checkbox]').is(':checked');//判断checkbox是否勾选，勾选返回True
        let data={
            'user_account':user_mobile,
            'password':password,
            'status':status
        }
        $.ajax({
            url:'/user1/login/',
            type:'POST',
            data:JSON.stringify(data),
            contentType:'application/json;charset=utf-8',
            dataType:'json'
        })
            .done(function (res){
                if (res.errno==='0') {
                    message.showSuccess(res.errmsg)
                    setTimeout(function (){
                        window.location.href='/index/';
                    },2000);
                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function (){
                message.showError('请求超时')
            });

    });


})