var ip="localhost" 

var app_subject_demo = new Vue({
    el: '#subject_demo',
    data:{
        lecture_list: "加载中..."
    },
    mounted: function get_lecture(){
        $.ajax({
            type: 'POST',
            url: 'http://'+ip+':5000/api/get_lecture_by_subject',
            data: {
                subject: document.title
            },
          success: function (response) {
            response=JSON.parse(response);
              if(response){
                app_subject_demo.lecture_list=response.lecture_list;
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

var app_search_demo = new Vue({
    el: '#search_demo',
    data:{
        lecture_list: "加载中..."
    },
    mounted: function get_lecture(){
        $.ajax({
            type: 'POST',
            url: 'http://'+ip+':5000/api/get_lecture_by_keyword',
            data: {
                keyword: document.title
            },
          success: function (response) {
            response=JSON.parse(response);
              if(response){
                app_search_demo.lecture_list=response.lecture_list;
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