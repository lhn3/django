/*=== bannerStart ===*/
//轮播图
$(()=>{
    fn_load_banner()
    let $banner = $('.banner');
    let $picLi = $(".banner .pic li");
    let $prev = $('.banner .prev');
    let $next = $('.banner .next');
    let $tabLi = $('.banner .tab li');
    let index = 0;
    // 小原点
    $tabLi.click(function(){
        index = $(this).index();
        $(this).addClass('active').siblings('li').removeClass('active');
        $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500);
    });
    // 点击切换上一张
    $prev.click(()=>{
        index--;
        if(index<0){index = $tabLi.length-1}
        $tabLi.eq(index).addClass('active').siblings('li').removeClass('active');
        $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500);
    }).mousedown(()=> false);
    // 点击切换下一张
    $next.click(()=>{
        auto();
    }).mousedown(()=> false);
    //  图片向前滑动
    function auto(){
        index++;
        index %= $tabLi.length;
        $tabLi.eq(index).addClass('active').siblings('li').removeClass('active');
        $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500);
    }
    // 定时器
    let timer = setInterval(auto, 2500);
    $banner.hover(()=>{clearInterval(timer)}, ()=>{auto()})

/*=== bannerEnd ===*/
/*=== newsNavStart ===*/
$(()=>{
    let $newsLi = $('.news-nav ul li');
    $newsLi.click(function(event) {
        $(this).addClass('active').siblings('li').removeClass('active');
    });
});

      function fn_load_banner() {
        $.ajax({
          // 请求地址
          url: "/banner/",  // url尾部需要添加/
          // 请求方式
          type: "GET",
          async: false
        })
          .done(function (res) {
            if (res.errno === "0") {
              let content = `` ;
              let tab_content = ``;   //按钮
              res.data.banners.forEach(function (one_banner, index) {
                if (index === 0){
                  // 需要修改 href  接收后台传来的id号 响应详情页  one_banner.news_id
                  content = `
                    <li style="display:block;"><a href="/news_detail/${one_banner.news_id}/" target="_blank">
                     <img src="${one_banner.image_url}" alt="${one_banner.news_title}"></a></li>
                  `;
                  tab_content = `<li class="active"></li>`;
                } else {
                  content = `
                  <li><a href="/news_detail/${one_banner.news_id}/" target="_blank"><img src="${one_banner.image_url}" alt="${one_banner.news_title}"></a></li>
                  `;
                  tab_content = `<li></li>`;
                }

                $(".pic").append(content);  // 内容
                $(".tab").append(tab_content); // 标签
              });

            } else {
              // 登录失败，打印错误信息
              message.showError(res.errmsg);
            }
          })
          .fail(function () {
            message.showError('服务器超时，请重试！');
          });
      }
/*=== newsNavEnd ===*/







$(function (){
    //新闻列表功能
    let $news_list=$('.news-nav ul li');
    let page=1;  //默认第一页
    let total_page=1; //默认总页数为1
    let tag_id=0; //默认分类标签为0
    let is_load_data=true; //是否正在向后台加在数据

      //定义向后端获取新闻列表数据的请求
    function fn_content() {
        // let sCurrentTagId = $('.active a').attr('data-id');
        //创建请求参数
        let Data={
            'tag_id':tag_id,
            'page':page
        };
        $.ajax({
            url:'/news/',
            type:'GET',
            data:Data,
            dataType:'json',
        })
            .done(function (res){
                if (res.errno==='0'){
                    total_page=res.data.total_pages;
                    if (page===1){
                        $('.news-list').html('')
                    }
                    res.data.news.forEach(function (one_news){
                        let content=`
                        <li class="news-item">
                 <a href="/news_detail/${one_news.id}/" class="news-thumbnail" target="_blank">
                    <img src="${one_news.image_url}" alt="${one_news.title}" title="${one_news.title}">
                 </a>
                 <div class="news-content">
                    <h4 class="news-title"><a href="/news_detail/${one_news.id}/" target="_blank">${one_news.title}</a></h4>
                    <p class="news-details">${one_news.digest}</p>
                    <div class="news-other">
                      <span class="news-type">${one_news.tag_name}</span>
                      <span class="news-time">${one_news.update_time}</span>
                      <span class="news-author">${one_news.author}</span>
                    </div>
                 </div>
              </li>`;
                        $('.news-list').append(content)
                    });
                    $('.news-list').append($('<a href="javascript:void(0);" class="btn-more">滚动加载更多</a>'));
                    //数据加载完毕，设置正在加在数据的变量为false，表示当前没有在加在数据
                    is_load_data=false;
                }else{
                    message.showError(res.errmsg)
                }
            })
            .fail(function (){
                message.showError('服务器超时')
            })
    }

    fn_content();

    $news_list.click(function (){
        //点击分类标签，则为点击的标签加上一个class属性为active
        //并且移除其他兄弟元素上值为activate的class属性

        $(this).addClass('activate').siblings('li').removeClass('activate');
        //获取绑定在当前选中分类上的data-id属性值
        let click_tag=$(this).children('a').attr('data-id');

        if (click_tag !== tag_id){
            tag_id=click_tag;  //记录当前分类ID
            //重置分页参数
            page=1;
            total_page=1;
            fn_content()
        }
    });

    //页面滚动加载
     $(window).scroll(function () {
        // 浏览器窗口高度
        let showHeight = $(window).height();
        // 整个网页的高度
        let pageHeight = $(document).height();
        // 页面可以滚动的距离
        let canScrollHeight = pageHeight - showHeight;
        // 页面滚动了多少,这个是随着页面滚动实时变化的
        let nowScroll = $(document).scrollTop();
        if ((canScrollHeight - nowScroll) < 100) {
          // 判断页数，去更新新闻数据
            if (!is_load_data) {
            is_load_data = true;
            // 如果当前页数据如果小于总页数，那么才去加载数据
            if (page < total_page) {
              page += 1;
              $(".btn-more").remove();  // 删除标签
              // 去加载数据
              fn_content()
            } else {
              message.showInfo('已全部加载，没有更多内容！');
              $(".btn-more").remove();  // 删除标签
              $(".news-list").append($('<a href="javascript:void(0);" class="btn-more">已全部加载，没有更多内容！</a>'))
            }
          }
        }
      });

})



});