# 模板使用记录
## 版权问题
[声明版权使用权限的网址](https://www.os-templates.com/template-terms)   
根据该网址关于免费模板的版权限制，需要在网站中保留版权声明   

## 修改记录
### 2020.11.24
1. 修改了头部和导航页

![2020-11-24_160116](http://img.joycez.xyz/md/2020-11-24_160116.jpg)

2. 删除了尾部明显不需要的部分

![2020-11-24_160317](http://img.joycez.xyz/md/2020-11-24_160317.jpg)

3. 同步修改了一个学科页demo

![2020-11-24_160506](http://img.joycez.xyz/md/2020-11-24_160506.jpg)

### 2020.12.9   
目前最新部署的网页地址为：http://111.229.84.244:5000/
1. 修改了网页配色
2. 合并了导航栏
3. 添加了搜索框
4. 使用Flask，采取前后端不分离方式改写了网站demo   
    目前网站文件结构如下：
    ```python
    Flask
        | - api.py (flask APP)
        | - templates (模板文件夹)
        |           | - index.html (首页模板)
        |           | - search_demo.html (搜索结果页模板)
        |           | - subject_demo.html (学科页模板)
        |
        | - static (静态文件文件夹)
                | - images (图片文件夹)
                | - layout (布局文件夹)
                |       | - srcipts (js文件夹)
                |       | - styles (css文件夹)
                |
                | - pages  (备用页面文件夹)

    ```

5. 实现两个将数据库搜索结果回传到页面上的demo   
    使用的SQL语句如下，对应学科导航栏和搜索框
    
    ```mysql
    # 根据学科返回所有讲座信息
    select title,organizer,introduction from lecture where field like '%{field}%'
    # 根据关键词返回标题中包含关键词的讲座信息
    select title,organizer,introduction,field
    from lecture 
    where title like '%{keyword}%';
    ```

### 2021.3.7

新增了轮播图和日历功能

![2021-03-07_204927](http://img.joycez.xyz/md/2021-03-07_204927.jpg)

![2021-03-07_204938](http://img.joycez.xyz/md/2021-03-07_204938.jpg)