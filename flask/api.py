from flask import Flask, request, render_template, jsonify
from flask_cors import *
from text_module import Text,subtitle
import time
import pymysql
import json
import copy

app = Flask(__name__,static_url_path='/static/',template_folder='templates')
CORS(app, resources=r'/*')

mysql_path="82.156.28.161"
mysql_user="mysql"
mysql_pass="xiaochuang12345"
mysql_db="xiaochuang"

ip="localhost:5000"
img_url="localhost:8080/img"

reverse_subtitle={'新闻传播': 'journalism', '工学': 'engineering', 
'艺术': 'art', '历史': 'history', '文学': 'literature', 
'自然科学': 'natural', '经济学': 'economics', 
'教育学': 'education', '工商管理': 'management', 
'传播学': 'communication', '哲学': 'philosophy', '法学': 'law',"其他":"others"}

# GET
###################################################################################################
@app.route('/api/get_wechat_notes', methods=['GET'])
def get_wechat_notes():
    '''
    对应首页轮播图数据
    返回微信公众号头图及其链接
    '''
    # 最好把数据存在数据库里
    notes_list=[
        {
            "image":"http://"+img_url+"/八大作_fit.png",
            "url":"https://mp.weixin.qq.com/s/W18r_ypMjprtecjJAbDarw"
        },
        {
            "image":"http://"+img_url+"/谏逐客书_fit.png",
            "url":"https://mp.weixin.qq.com/s/6eCGNFpzEhDNiTHzvIc2Zg"
        },
        {
            "image":"http://"+img_url+"/媒体融合和解构_fit.png",
            "url":"https://mp.weixin.qq.com/s/rlX3hESuEwdozY9Ava6jBg"
        },
        {
            "image":"http://"+img_url+"/数字经济_fit.png",
            "url":"https://mp.weixin.qq.com/s/NMOTOvcO0Bw-ykwDe4gStw"
        },
        {
            "image":"http://"+img_url+"/新基建_fit.png",
            "url":"https://mp.weixin.qq.com/s/a00FFJn5um38mjhCwKFPfg"
        }
    ]

    return json.dumps({'notes_list':notes_list},ensure_ascii=False)

@app.route('/api/get_trending', methods=['GET'])
def get_trending():
    '''
    对应首页热搜数据
    返回由算法得出的热搜讲座信息
    '''
    # 热搜算法还没设计，随机从数据库中抽取四个讲座信息
    db = pymysql.connect(host=mysql_path, user=mysql_user, password=mysql_pass, database=mysql_db)
    cursor = db.cursor()
    sql="""SELECT ID, title, starttime
    FROM lecture ORDER BY rand() LIMIT 4;"""
    cursor.execute(sql)
    data=cursor.fetchall()

    trending_list=[]
    for lecture in data:
        info={
            "title":lecture[1] if len(lecture[1])<16 else lecture[1][:16]+"...",
            "date":str(lecture[2])[:10],
            "url":"http://"+ip+"/lecture="+str(lecture[0])
        }
        trending_list.append(info)
    return json.dumps({'trending_list':trending_list},ensure_ascii=False)

@app.route('/api/get_trending_by_subject', methods=['GET'])
def get_trending_by_subject():
    '''
    对应学科页热搜数据
    返回由算法得出的热搜讲座信息
    '''
    # 热搜算法还没设计，随机从数据库中抽取四个讲座信息

    field=reverse_subtitle[request.args['field']]

    db = pymysql.connect(host=mysql_path, user=mysql_user, password=mysql_pass, database=mysql_db)
    cursor = db.cursor()
    sql="""SELECT ID, title, starttime
    FROM lecture 
    where field='{}'
    ORDER BY rand() LIMIT 4;""".format(field)
    cursor.execute(sql)
    data=cursor.fetchall()

    trending_list=[]
    for lecture in data:
        info={
            "title":lecture[1] if len(lecture[1])<16 else lecture[1][:16]+"...",
            "date":str(lecture[2])[:10],
            "url":"http://"+ip+"/lecture="+str(lecture[0])
        }
        trending_list.append(info)
    return json.dumps({'trending_list':trending_list},ensure_ascii=False)

@app.route('/api/get_notice', methods=['GET'])
def get_notice():
    '''
    对应首页讲座预告数据
    返回最近的四个未开始讲座
    '''
    # 预告数据还没收集，从数据库中选出时间最近的四个讲座信息
    db = pymysql.connect(host=mysql_path, user=mysql_user, password=mysql_pass, database=mysql_db)
    cursor = db.cursor()
    sql="""SELECT ID, title
    FROM lecture ORDER BY starttime desc LIMIT 4;"""
    cursor.execute(sql)
    data=cursor.fetchall()

    notice_list=[]
    for lecture in data:
        info={
            "title":lecture[1] if len(lecture[1])<25 else lecture[1][:25]+"...",
            "url":"http://"+ip+"/lecture="+str(lecture[0])
        }
        notice_list.append(info)

    return json.dumps({'notice_list':notice_list},ensure_ascii=False)

@app.route('/api/get_content',methods=['GET'])
def get_content():
    '''
    返回查找id对应的内容
    '''
    ID=request.args['ID']
    result=get_detail_by_id(ID)

    return json.dumps({'title':result['title'],
        'content':result['total_content'],
        'url':"http://"+ip+"/lecture="+str(ID)},ensure_ascii=False)

# 模板渲染
###################################################################################################
# 主页
@app.route('/')
def index():
    return render_template("index.html")

# 学科页
@app.route('/subject=<subject>')
def direct_to_subject_page(subject):
    db = pymysql.connect(host=mysql_path, user=mysql_user, password=mysql_pass, database=mysql_db)
    cursor = db.cursor()
    sql = """
    select ID,title,date_format(starttime,'%Y-%m-%d') 
    from lecture where field = '{}'
    order by starttime DESC;
    """.format(subject)
    cursor.execute(sql)
    data = cursor.fetchall()

    lecture_list = []

    for i in data:
        temp = {}
        if len(i[1])<=40:
            temp['title'] = i[1]
        else:
            temp['title'] = i[1][:40]+'...'
        temp['time'] = i[2]
        temp['url'] = "http://"+ip+"/lecture="+str(i[0])
        lecture_list.append(copy.deepcopy(temp))
    # 为网页加title
    if(subject not in subtitle.keys()):
        subtitle[subject]="今日人文社科"

    return render_template("subject.html", title=subtitle[subject],lecture_list=lecture_list)

# 搜索结果页
@app.route('/search=<keyword>')
def direct_to_search_page(keyword):
    db = pymysql.connect(host=mysql_path, 
                        user=mysql_user, 
                        passwd=mysql_pass, 
                        db=mysql_db)
    cursor = db.cursor()
    sql="""
    select title,ID
    from lecture 
    where title like '%{}%';
    """.format(keyword)

    cursor.execute(sql)
    data=cursor.fetchall()
    db.close()

    result_list=[]
    
    if len(data) == 0:
        # 没有搜索结果
        return render_template('search_404.html',
                            title = "关键词\t"+keyword+"\t搜索结果：0条")
    else:
        for i in data:         
            temp={}
            temp['title']=i[0]
            temp['ID']=i[1]
            result_list.append(copy.deepcopy(temp))

        result = get_detail_by_id(result_list[0]['ID'])
        result['url']="http://"+ip+"/lecture="+str(result_list[0]['ID'])
        length = len(result_list)

    return render_template('search.html',
                            keyword = keyword,
                            result = result,
                            length = length,
                            result_list = result_list)

# 日期跳转页
@app.route('/date=<date>')
def direct_to_date_page(date):
    """
    对应日期的讲座列表
    """
    db = pymysql.connect(host=mysql_path, 
                        user=mysql_user, 
                        passwd=mysql_pass, 
                        db=mysql_db)
    cursor = db.cursor()
    sql="""
    select title,ID
    from lecture 
    where DATE(starttime)= '{}';
    """.format(date)

    cursor.execute(sql)
    data=cursor.fetchall()
    db.close()

    result_list=[]
    
    if len(data) == 0:
        # 没有搜索结果
        return render_template('date_404.html',
                            title = "日期\t"+date+"\t收录结果：0条")
    else:
        for i in data:         
            temp={}
            temp['title']=i[0]
            temp['ID']=i[1]
            result_list.append(copy.deepcopy(temp))

        result = get_detail_by_id(result_list[0]['ID'])
        
        result['url']="http://"+ip+"/lecture="+str(result_list[0]['ID'])
        length = len(result_list)

    return render_template('date.html',
                            date = date,
                            result = result,
                            length = length,
                            result_list = result_list)

# 内容页
@app.route('/lecture=<ID>')
def direct_to_lecture_page(ID):
    '''
    讲座详细内容页面
    '''
    result=get_detail_by_id(ID)
    return render_template('content.html',result=result)

    return data

# 根据lecture id查询文章详细内容
def get_detail_by_id(ID):
    # db = pymysql.connect(host=mysql_path, 
    #                     user=mysql_user, 
    #                     passwd=mysql_pass, 
    #                     db=mysql_db)
    # cursor = db.cursor()
    # sql="""
    # select ID,title,organizer,starttime,
    # location,field,introduction
    # from lecture 
    # where ID ={};
    # """.format(ID)

    # cursor.execute(sql)
    # data=cursor.fetchall()[0]
    # db.close()

    # content=data[6] if data[6] != '' else "暂无"

    # return {"ID":data[0],"title":data[1],
    # "organizer":data[2],"start":data[3],"location":data[4],
    # "field":data[5],"intro":content}
    text=Text(ID)
    text.func()
    return text.my_dict

# my_text = Text(lecture_id)
#     content = my_text.func()

#     return content  # 返回值为讲座介绍文本

if __name__ == '__main__':
    app.debug=True
    app.run('0.0.0.0', 5000)