var ip="0.0.0.0"
$('#search').on('keypress',function(event){
    // 搜索框回车跳转到搜索结果页
    if(event.keyCode == 13)      
    {  
        var url = "http://"+ip+":5000/search="+$('#search').val()
        window.location.href=url;
    }  
});

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
