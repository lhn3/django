
$(function () {
    let image_uuid='';
    let mobile_flag=false;
    let username_flag=false;
    let send_flag=true
    //验证码图片验证
    let $image=$('.captcha-graph-img img');
    image_check();
    $image.click(image_check);
    function image_check(){
        image_uuid = generateUUID();
        let image_url='/ver/image/'+image_uuid+'/';
        $image.attr('src',image_url);
    }

// uuid
    function generateUUID() {
    let d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
    }

    //用户名验证
    let $usernam=$('#user_name');
    $usernam.blur(username_check);
    function username_check(){
        let user_name=$usernam.val();
        if (!user_name===''){
            message.showError('请输入用户名');
            return
        }
        if (!(/[\u4e00-\u9fa5\w]{3,10}$/).test(user_name)){
            message.showError('用户名格式错误');
            return
        }
        $.ajax({
            url:'/ver/username/'+user_name+'/',
            type:'GET',
            dataType:'json'
        })
            .done(function (res){
                // if (res['count']){
                if (res.data.count){
                    message.showError('用户名已存在')
                }else {message.showSuccess('用户名可以使用')
                    username_flag=true;
                }
            })
            .fail(function (){
                    message.showError('请求超时')
                })
    }

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
                if (res.data.count){
                    message.showError('此号码已被注册');
                }else {
                    message.showSuccess('此号码可正常使用');
                    mobile_flag=true;
                }
            })
            .fail(function (){
                message.showError('请求超时');
            })
    }
//短信发送
    let $sms=$('.sms-captcha'); //获取发送验证码按钮
    let $images=$('#input_captcha'); //输入的验证码值
    $sms.click(function (){
        if(send_flag===true){
            send_flag=false
            if (username_flag===false){
                username_check();
                return;
            }
            if (mobile_flag===false){
                mobile_check();
                return;
            }
            let text=$images.val();
            if (text===''){
                message.showError('请输入验证码');
                return;
            }
            if (image_uuid===''){
                message.showError('图形UUID为空');
                return;
            }
            let Data={             //字典格式
                'mobile':$mobile.val(),
                'text':text,
                'uuid':image_uuid,
                'p':'1'
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

//注册用户
    let $btn=$('.form-contain'); //获取表单数据
    $btn.submit(function (e){   //提交事件
        e.preventDefault();         //阻止默认提交操作
        //取到表单中用户名，密码，电话，短信验证码的值
        let username_sub=$('#user_name').val();
        let password_sub=$('#pwd').val();
        let password2_sub=$('input[name=password_repeat]').val();
        let mobile_sub=$('#mobile').val();
        let sms_sub=$('#input_smscode').val();
        //验证用户名，手机号码，密码是否输入并符合要求
        if (!username_flag){
            username_check();
            return
        }
        if (!mobile_flag){
            mobile_check();
            return
        }
    // const reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[\x21-x7e]{6,18}$/
    // 以首字母开头，必须包含数字的6-18位
    // 判断用户输入的密码和确认密码长度是否为6-20位
        if (password_sub==='') {
            message.showError('密码不能为空');
            return
        }
        if (!(/^[0-9a-zA-Z]{6,18}$/).test(password_sub)){
            message.showError('密码格式错误，请输入6-18位密码');
            return
        }
        if (password2_sub==='') {
            message.showError('确认密码不能为空');
            return
        }
        if (password_sub !== password2_sub){
            message.showError('两次密码不一致，请重新输入')
            return
        }
        //判断短信验证码是否输入并符合要求
        if (sms_sub===''){
            message.showError('短信验证码不能为空');
            return
        }
        if (!(/^[0-9]{6}$/).test(sms_sub)){
            message.showError('验证码格式错误，请输入六位数字验证码');
            return
        }

        let Data_sub={
            'username':username_sub,
            'password':password_sub,
            'password_re':password2_sub,
            'mobile':mobile_sub,
            'sms_code':sms_sub
        }
        $.ajax({
            url:'/user1/register/',
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
                        window.location.href='/index/';
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

