var ip="localhost"

var app_date = new Vue({
    el: '#DateApp',
    data:{
        date: new Date()
    },
    mounted: function(){
        var _this=this;
        this.timer=setInterval(function(){
            _this.date = new Date();
        }, 1000);
    },
    beforeDestory: function(){
        if(this.timer){
            clearInterval(this.timer);
        }
    }
  });

var app_subject_list = new Vue({
    el: '#subject_list',
    data: {
        subject_list: []
    },
    mounted: function get_subject_list(){
        $.ajax({
            type: 'GET',
            url: 'http://'+ip+':5000/api/get_subject_list',
          success: function (response) {
              response=JSON.parse(response);
              if(response){
                  app_subject_list.subject_list=response.subject_list;
              }
              else{
                alert("nothing return！");
              }
          },
          error: function(XMLHttpRequest, textStatus, errorThrown){
              alert("Something Wrong!");
          }
          });
    }
})

$('#search').on('keypress',function(event){
    // 搜索框回车跳转到搜索结果页
    if(event.keyCode == 13)      
    {  
        var url = "http://"+ip+":5000/search="+$('#search').val()
        window.location.href=url;
    }  
});
