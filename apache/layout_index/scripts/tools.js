var ip="82.156.28.161"
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