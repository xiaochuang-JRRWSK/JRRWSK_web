var ip="0.0.0.0"
$('#search').on('keypress',function(event){
    // 搜索框回车跳转到搜索结果页
    if(event.keyCode == 13)      
    {  
        var url = "http://"+ip+":5000/search="+$('#search').val()
        window.location.href=url;
    }  
});
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

// 实现日历
// 参考：https://www.jq22.com/webqd5197
var month_olympic = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
var month_normal = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
var month_name = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];
var holder = document.getElementById("days");
var prev = document.getElementById("prev");
var next = document.getElementById("next");
var ctitle = document.getElementById("calendar-title");
var cyear = document.getElementById("calendar-year");
var my_date = new Date();
var my_year = my_date.getFullYear();
var my_month = my_date.getMonth();
var my_day = my_date.getDate();
prev.onclick = function(e) {
    e.preventDefault();
    my_month--;
    if (my_month < 0) {
        my_year--;
        my_month = 11;
    }
    refreshDate();
}
next.onclick = function(e) {
    e.preventDefault();
    my_month++;
    if (my_month > 11) {
        my_year++;
        my_month = 0;
    }
    refreshDate();
}

function refreshDate() {
    var str = "";
    var totalDay = daysMonth(my_month, my_year); //获取该月总天数
    var firstDay = dayStart(my_month, my_year); //获取该月第一天是星期几
    var myclass;
    var myhref;
    for (var i = 1; i < firstDay; i++) {
        str += "<li></li>"; //为起始日之前的日期创建空白节点
    }
    for (var i = 1; i <= totalDay; i++) {
        if ((i < my_day && my_year == my_date.getFullYear() && my_month == my_date.getMonth()) || my_year < my_date.getFullYear() || (my_year == my_date.getFullYear() && my_month < my_date.getMonth())) {
            myclass = " class='lightgrey'"; //当该日期在今天之前时，以浅灰色字体显示
        } else if (i == my_day && my_year == my_date.getFullYear() && my_month == my_date.getMonth()) {
            myclass = " class='calendar_color_box'"; //当该日期是当天时，以背景突出显示
        } else {
            myclass = " class='darkgrey'"; //当该日期在今后之后时，以深灰字体显示
        }
        myhref="<a href='#'>";
        str += "<li" + myclass + ">" + myhref + i + "</a></li>"; //创建日期节点
    }
    holder.innerHTML = str; //设置日期显示
    ctitle.innerHTML = month_name[my_month]; //设置中文月份显示
    cyear.innerHTML = my_year; //设置年份显示
}
//获取某年某月第一天是星期几
function dayStart(month, year) {
    var tmpDate = new Date(year, month, 1);
    return (tmpDate.getDay());
}

//计算某年是不是闰年，通过求年份除以4的余数即可
function daysMonth(month, year) {
    var tmp = year % 4;
    if (tmp == 0) {
        return (month_olympic[month]);
    } else {
        return (month_normal[month]);
    }
}
refreshDate();
