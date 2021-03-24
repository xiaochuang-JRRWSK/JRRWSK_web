from flask import Flask, request, render_template, jsonify
from flask_cors import *
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
            "image":"http://img.joycez.xyz/md/demo_banner.jpg",
            "url":"https://mp.weixin.qq.com/s/fGAQrtkfxVo1eeA249m7vg"
        },
        {
            "image":"http://img.joycez.xyz/md/demo_banner02.png",
            "url":"https://mp.weixin.qq.com/s/6eCGNFpzEhDNiTHzvIc2Zg"
        },
        {
            "image":"http://img.joycez.xyz/md/demo_banner03.png",
            "url":"https://mp.weixin.qq.com/s/rlX3hESuEwdozY9Ava6jBg"
        },
        {
            "image":"http://img.joycez.xyz/md/demo_banner04.png",
            "url":"https://mp.weixin.qq.com/s/NMOTOvcO0Bw-ykwDe4gStw"
        },
        {
            "image":"http://img.joycez.xyz/md/demo_banner05.png",
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
            "title":lecture[1],
            "date":str(lecture[2])[:10],
            "url":"http://"+ip+"/lecture/"+str(lecture[0])
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
            "title":lecture[1],
            "url":"http://"+ip+"/lecture/"+str(lecture[0])
        }
        notice_list.append(info)

    return json.dumps({'notice_list':notice_list},ensure_ascii=False)

# 模板渲染
###################################################################################################
@app.route('/')
def index():
    '''
    主页
    '''
    return render_template("index.html")

# @app.route('/subject/<subject>')
# def direct_to_subject_page(subject):
#     '''
#     学科页
#     '''
#     return render_template("subject_demo.html",title = subject)

# @app.route('/search=<keyword>')
# def direct_to_search_result_page(keyword):
#     '''
#     搜索结果页
#     '''
#     return render_template("search_demo.html",title = keyword)
@app.route('/lecture/<ID>')
def direct_to_lecture_page(ID):
    '''
    讲座详细内容页面
    '''
    db = pymysql.connect(host=mysql_path, user=mysql_user, password=mysql_pass, database=mysql_db)
    cursor = db.cursor()
    sql="""select content from message_text
    where ID={};""".format(ID)
    cursor.execute(sql)
    data=cursor.fetchall()[0][0]

    return data



if __name__ == '__main__':
    app.debug=True
    app.run('0.0.0.0', 5000)