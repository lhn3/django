$(function () {
//添加
  let $tagSelect = $("#category-select");   // 获取选择分类标签元素
  let $newsSelect = $("#news-select");      // 获取选择文章标签元素
  let $saveBtn = $('#save-btn');            // 获取保存按钮元素

  // 选择文章不同类别，获取相应的文章
  $tagSelect.change(function () {
    // 获取当前选中的下拉框的value
    let sTagId = $(this).val();
    if (sTagId === '0') {
      $newsSelect.children('option').remove();
      $newsSelect.append(`<option value="0">--请选择文章--</option>`);
      return
    }
    // 根据文章分类id向后端发起get请求
    $.ajax({
      url: "/admin/news_select/" + sTagId + "/",  // url尾部需要添加/
      type: "GET",
      dataType: "json",
    })
      .done(function (res) {
        if (res.errno === "0") {

          $newsSelect.children('option').remove();
          $newsSelect.append(`<option value="0">--请选择文章--</option>`);
          res.data.news.forEach(function (one_news) {
            let content = `<option value="${one_news.id}">${one_news.title}</option>`;
            $newsSelect.append(content)
          });

        } else {
          // swal.showInputError(res.errmsg);
          message.showError(res.errmsg);
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });

  });

  // 点击保存按钮执行的事件
  $saveBtn.click(function () {
    // 获取优先级
    let priority = $("#priority").val();
    // 获取下拉框中选中的文章标签id 和 文章id
    let sTagId = $tagSelect.val();
    let sNewsId = $newsSelect.val();
    // 判断是否为 0, 表示在第一个 未选择
    if (sTagId !== '0' && sNewsId !== '0' && priority !== '0') {

      let sDataParams = {
        "priority": priority,
        "news_id": sNewsId
      };

      $.ajax({
        // 请求地址
        url: "/admin/admin_hot/",  // url尾部需要添加/
        // 请求方式
        type: "POST",
        data: JSON.stringify(sDataParams),
        // 请求内容的数据类型（前端发给后端的格式）
        contentType: "application/json; charset=utf-8",
        // 响应数据的格式（后端返回给前端的格式）
        dataType: "json",
      })
        .done(function (res) {
          if (res.errno === "0") {
            message.showSuccess("热门文章创建成功");

            setTimeout(function () {
              window.location.href = '/admin/admin_hot/';
            }, 1500)
          } else {
            // swal.showInputError(res.errmsg);
            fAlert.alertErrorToast(res.errmsg);
          }
        })

        .fail(function () {
          message.showError('服务器超时，请重试！');
        });

    } else {
      fAlert.alertErrorToast("文章分类、文章以及优先级都要选择！");
    }
  });



    //编辑
    let $edit=$('.btn-edit');
        $edit.click(function (){     //点击事件
            let new_id=$(this).parents('tr').data('id');
            let new_name=$(this).parents('tr').data('name');
            let new_priority=$(this).data('priority');
        fAlert.alertOneInput({          //自定义弹窗事件
            title:'正在编辑'+'【'+new_name+'】'+'的优先级',
            text:'优先级设置请输入数字（1,2,3）',
            placeholder:'请输入文章优先级',
            confirmCallback:function confirmCallback(inp){
                if (inp==new_priority){
                    swal.showInputError('优先级未改变')
                    return
                }
                if (!(/^[1-3]{1}$/).test(inp)){
                    swal.showInputError('输入有误，请重新输入')
                    return
                }
                let Data={
                    'new_priority':inp
                };
                $.ajax({
                    url:'/admin/admin_rehot/'+new_id+'/',
                    type:'PUT',
                    data:JSON.stringify(Data),
                    contentType:'application/json;charset=utf-8',
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



    //删除
    let $del=$('.btn-del');
        $del.click(function (){     //点击事件
            let new_id=$(this).parents('tr').data('id');
            let new_name=$(this).parents('tr').data('name')
        fAlert.alertConfirm({ //自定义弹窗事件
            title:'确定删除'+'【'+new_name+'】'+'热门新闻吗？',
            type:'error',
            confirmButtonText:'确定',
            cancelButtonText:'取消',
            confirmCallback:function confirmCallback(){
                $.ajax({
                    url:'/admin/admin_delhot/'+new_id+'/',
                    type:'DELETE',
                    dataType:'json'
                })
                    .done(function (res){
                        if (res.errno==='0'){
                            fAlert.alertSuccessToast(res.errmsg)
                            setTimeout(function (){
                                window.location.reload();
                            },500)
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

