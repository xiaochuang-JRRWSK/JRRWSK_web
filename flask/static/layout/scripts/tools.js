var ip="localhost"
$('#search').on('keypress',function(event){
    // 搜索框回车跳转到搜索结果页
    if(event.keyCode == 13)      
    {  
        var url = "http://"+ip+":5000/search="+$('#search').val()
        window.location.href=url;
    }  
});

$.fn.smartFloat = function() {
    var position = function(element) {
     var top = element.position().top, pos = element.css("position");
     $(window).scroll(function() {
      var scrolls = $(this).scrollTop();
      if (scrolls > top) {
       if (window.XMLHttpRequest) {
        element.css({
         position: "fixed",
         top: 0
        }); 
       } else {
        element.css({
         top: scrolls
        }); 
       }
      }else {
       element.css({
        position: pos,
        top: top
       }); 
      }
     });
    };
    return $(this).each(function() {
     position($(this));      
    });
};

