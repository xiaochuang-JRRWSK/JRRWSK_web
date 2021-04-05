get_wechat_notes();
// get_trending();
// 获取数据
function get_wechat_notes(){
    // 获取微信公众号文章
    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/get_wechat_notes',
        success: function (response) {
          response=JSON.parse(response);
          if(response){
              show_wechat_notes(response['notes_list']);
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

function get_trending(){
    // 获取热搜数据
    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/get_trending',
        success: function (response) {
          response=JSON.parse(response);
          if(response){
              show_trending(response['trending_list']);
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

// 显示数据
function show_wechat_notes(notes_list){
    let index=0;
    $('div#banner').find('a').each(function(){
        $(this).attr('href',notes_list[index]['url']);
        $(this).find('img').attr('src',notes_list[index]['image']);
        index++;
    })
}
function show_trending(trending_list){
    let index=0;
    $('div#trending').find('div').each(function(){
        $(this).append("<a href="+trending_list[index]['url']+">"
        +trending_list[index]['title']+"</a>");
        index++;
    })
}