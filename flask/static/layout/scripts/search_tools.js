// 点击的文本让内容框变成对应的内容
function get_content(id){
    // 获取微信公众号文章
    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/get_content',
        data:{ID:id},
        dataType: "json",
        success: function (response) {
          // 此处使用parse方法会报错
          if(response){
            response=JSON.stringify(response);
            response=JSON.parse(response);
            
            show_content(response);
          }
          else{
            alert("nothing return！");
          }
      },
        error: function(XMLHttpRequest, textStatus, errorThrown){
          alert("Something Wrong!");
      }
});
    
    $('#content-list').find('p').each(function(){
        $(this).attr('style','color:#000000');
    });
    $('#'+id).attr('style','color:#3e7fd3');

}

function show_content(response){
    $('#content-box').find('a').text(response['title']);
    $('#content-box').find('a').attr('href',response['url']);
    //$('#content-box').find('p').text(response['content']+"<br>hhh");
    document.getElementById('content-box').getElementsByTagName('p')[0].innerHTML=response['content'];
}