// 选中标题变色
var mytitle=$('title').text();
var flag=false;
$('#topbar').find('a').each(function(){
    if($(this).text()==mytitle){
        $(this).attr('style','color:#003366');
        return false;
    }
    else if($(this).text()=="首页" && mytitle=="今日人文社科"){
        $(this).attr('style','color:#003366');
        return false;
    }
});

// 实现轮播图
// 参考：https://www.sucainiu.com/code/1755.html
function carousel(stop_time) {
    var $carousel = $('.carousel > .carousel-inner > .item'); // 轮播内容
    var length = $carousel.length - 1; // 从0开始
    var next = 0;
    var prev = 0;
    var $sort = $('.carousel > .carousel-sort > .item'); // 当前进度

    // 获取当前的active
    function current_active() {
        for (var i = 0; i < $carousel.length; i++) {
            if ($($carousel[i]).hasClass('active')) {
                return i
            }
        }
    }

    // 添加active
    function add_active(next) {
        $($carousel[next]).addClass('active');
        $($sort[next]).addClass('active');
    }

    // 移除active
    function remove_active(prev) {
        $($carousel[prev]).removeClass('active');
        $($sort[prev]).removeClass('active');
    }

    // 下一张
    function run_next(num) {
        next += num;
        if (next > length) {
            next = 0;
        }
        return next
    }

    // 上一张
    function run_prev(num) {
        prev = next - num;
        if (prev < 0) {
            prev = length
        }
        return prev
    }

    // 根据时间，自动切换
    function run_carousel() {
        add_active(run_next(1));
        remove_active(run_prev(1));
    }

    // 定时
    var interval = null;

    function run_interval() {
        interval = setInterval(run_carousel, stop_time)
    }

    function stop_interval() {
        clearInterval(interval)
    }
    run_interval();

    // 切换进度
    $($sort).click(function() {
        stop_interval();
        remove_active(current_active());
        add_active($(this).index());
        next = current_active();
        run_interval()
    });

    // 鼠标悬停
    var mouse_tar = $($carousel).parent();
    $(mouse_tar).mouseenter(function() {
        stop_interval()
    });
    $(mouse_tar).mouseleave(function() {
        run_interval()
    });

    // 左右切换
    $('.carousel-left').click(function() {
        stop_interval();
        remove_active(current_active());
        var prev = run_prev(1);
        add_active(prev);
        next = prev;
        run_interval()
    });
    $('.carousel-right').click(function() {
        stop_interval();
        remove_active(current_active());
        add_active(run_next(1));
        run_interval()
    })
}
// 每次更换内容的时间
carousel(3000)


