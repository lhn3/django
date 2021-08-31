$(function (){
    let $course_data=$('course-data');
    let video_url=$course_data.data('video-url');
    let cover_url=$course_data.data('cover-url');

    let player = cyberplayer("course-video").setup({
        width: '100%',
        height: 480,
        file: video_url,
        image: cover_url,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        ak: 'aee47a29e8c345189b1f25f61590a724'
    });
})