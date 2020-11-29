var app = new Vue({
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