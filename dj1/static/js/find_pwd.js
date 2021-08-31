
$(function () {
    let mobile_flag=false;
    let send_flag=true

//手机号验证
    let $mobile=$('#mobile');
    $mobile.blur(mobile_check); //焦点事件
    function mobile_check(){
        let Mobile=$mobile.val();
        if (Mobile===''){
            message.showError('请输入手机号');
            return
        }
        if (!(/^1[3-9]\d{9}$/).test(Mobile)){
            message.showError('手机号码格式不正确')
            return
        }
        $.ajax({
            url: '/ver/mobile/'+Mobile+'/',
            type: 'GET',
            dataType: 'json'
        })
            .done(function (res){
                if (res.data.count===0){
                    message.showError('此号码未被注册');
                }else {
                    mobile_flag=true;
                }
            })
            .fail(function (){
                message.showError('请求超时');
            })
    }
//短信发送
    let $sms=$('.sms-captcha');
    $sms.click(function (){
        if(send_flag===true){
            send_flag=false;
            if (mobile_flag===false){
                mobile_check();
                return;
            }
            let Data={
                'mobile':$mobile.val(),
            }
            $.ajax({
                url:'/ver/sms/',
                type:'POST',
                data:JSON.stringify(Data),  //传入后端
                contentType:'application/json;charset=utf-8',
                headers: {'X-CSRFToken':getCookie('csrftoken')},
                dataType:'json'
            })
            .done(function (res){
                if (res.errno==='0'){
                    message.showSuccess(res.errmsg);
                    let num=60;
                    let t=setInterval(function (){
                        if (num===1){
                            clearInterval(t);
                            $sms.html('获取短信验证码');
                            send_flag=true;
                        }else {
                            num-=1;
                            $sms.html(num+'秒')
                        }
                    },1000)
                }else {
                    message.showError(res.errmsg);
                    send_flag=true;
                }
            })
                .fail(function (){
                    message.showError('请求超时');
                })
        }
    })

//提交修改密码表单
    let $btn=$('.form-contain');
    $btn.submit(function (e){
        e.preventDefault();
        let password_sub=$('#pwd').val();
        let mobile_sub=$('#mobile').val();
        let sms_sub=$('#input_smscode').val();
        if (!mobile_flag){
            mobile_check();
            return
        }
        if (password_sub==='') {
            message.showError('密码不能为空');
            return
        }
        if (!(/^[0-9a-zA-Z]{6,18}$/).test(password_sub)){
            message.showError('新密码格式错误，请输入6-18位密码');
            return
        }

        if (sms_sub===''){
            message.showError('短信验证码不能为空');
            return
        }
        if (!(/^[0-9]{6}$/).test(sms_sub)){
            message.showError('验证码格式错误，请输入六位数字验证码');
            return
        }
        let Data_sub={
            'password':password_sub,
            'mobile':mobile_sub,
            'sms_code':sms_sub
        }
        $.ajax({
            url:'/user1/find_pwd/',
            type:'POST',
            data: JSON.stringify(Data_sub),
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

