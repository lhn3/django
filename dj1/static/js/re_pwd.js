
$(function () {
//提交修改密码表单
    let $btn=$('.form-contain');
    $btn.submit(function (e){
        e.preventDefault();
        let pwd1=$('#pwd').val();
        let pwd2=$('input[name=password_repeat]').val();
        if (pwd1==='') {
            message.showError('旧密码不能为空');
            return
        }
        if (pwd2==='') {
            message.showError('新密码不能为空');
            return
        }
        if (!(/^[0-9a-zA-Z]{6,18}$/).test(pwd2)){
            message.showError('新密码格式错误，请输入6-18位密码');
            return
        }
        let data={
            'old':pwd1,
            'new':pwd2,
        }
        $.ajax({
            url:'/user1/re_pwd/',
            type:'POST',
            data: JSON.stringify(data),
            headers:{'X-CSRFToken':getCookie('csrftoken')},
            contentType: 'application/json;charset=utf-8',
            dataType:'json',
            })
            .done(function (res){
                if (res.errno==='0'){
                    message.showSuccess(res.errmsg);
                    setTimeout(function (){     //两秒后重定向到登录页面
                        window.location.href='/user1/login/';
                    },2000);
                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function (){
                message.showError('服务超时，请重试')
            })
    })

    //csrf认证
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
        }
        return cookieValue;
    }
})

