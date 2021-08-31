$(function (){
  //日历
      let $startTime = $("input[name=start_time]");
      let $endTime = $("input[name=end_time]");
      const config = {
        // 自动关闭
        autoclose: true,
        // 日期格式
        format: 'yyyy/mm/dd',
        // 选择语言为中文
        language: 'zh-CN',
        // 优化样式
        showButtonPanel: true,
        // 高亮今天
        todayHighlight: true,
        // 是否在周行的左侧显示周数
        calendarWeeks: true,
        // 清除
        clearBtn: true,
        // 0 ~11  网站上线的时候
        startDate: new Date(2018, 10, 1),
        // 今天
        endDate: new Date(),
      };
      $startTime.datepicker(config);
      $endTime.datepicker(config);

      //删除
      let $del=$('.btn-del');
      $del.click(function (){
        let news_id=$(this).data('id');
        let news_title=$(this).data('title');
        fAlert.alertConfirm({
          title:'确定删除'+'【'+news_title+'】'+'热门新闻吗？',
            type:'error',
            confirmButtonText:'确定',
            cancelButtonText:'取消',
            confirmCallback:function confirmCallback(){
                $.ajax({
                    url:'/admin/admin_delnews/'+news_id+'/',
                    type:'DELETE',
                    dataType:'json'

                })
                    .done(function (res){
                        if (res.errno==='0'){
                            fAlert.alertSuccessToast(res.errmsg)
                            setTimeout(function (){
                                window.location.reload();
                            },800)
                        }else {
                            swal.showInputError(res.errmsg);
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