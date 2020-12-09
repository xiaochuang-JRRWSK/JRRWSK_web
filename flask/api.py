from flask import Flask, request, render_template, jsonify
from flask_cors import *
import time
import pymysql
import json
import copy

app = Flask(__name__,static_url_path='/static/',template_folder='templates')
CORS(app, resources=r'/*')

mysql_path="111.229.84.244"
mysql_user="JJYDXFS"
mysql_pass="xiaochuang12345"
mysql_db="xiaochuang"

ip="localhost"

# 主页
@app.route('/')
def index():
    return render_template("index.html")

# GET

@app.route('/api/get_subject_list', methods=['GET'])
def get_subject_list():
    '''
    返回学科及学科url列表
    '''
    path="http://"+ip+":5000/"
    subject_list=[
        {
            'subject': '经济',
            'url': path+'subject/economics'
        },{
            'subject': '教育',
            'url': path+'subject/education'
        },{
            'subject': '艺术',
            'url': path+'subject/art'
        },{
            'subject': '文学',
            'url': path+'subject/literature'
        },{
            'subject': '管理学',
            'url': path+'subject/management'
        },{
            'subject': '传播',
            'url': path+'subject/communication'
        },{
            'subject': '哲学',
            'url': path+'subject/philosophy'
        },{
            'subject': '新闻',
            'url': path+'subject/journalism'
        },{
            'subject': '法律',
            'url': path+'subject/law'
        }
    ]

    return json.dumps({'subject_list':subject_list},ensure_ascii=False)

# POST

@app.route('/api/get_lecture_by_subject', methods=['POST'])
def get_lecture_by_subject():
    '''
    返回对应学科的讲座列表
    '''
    subject=request.form['subject']
    
    db = pymysql.connect(mysql_path, mysql_user, mysql_pass, mysql_db)
    cursor = db.cursor()
    sql="""
    select title,organizer,introduction from lecture where field like '%{}%';
    """.format(subject)
    cursor.execute(sql)
    data=cursor.fetchall()

    lecture_list=[]

    for i in data:
        temp={}
        temp['title']=i[0]
        temp['organizer']=i[1]
        temp['introduction']=i[2]
        lecture_list.append(copy.deepcopy(temp))

    return json.dumps({'lecture_list':lecture_list},ensure_ascii=False)

@app.route('/api/get_lecture_by_keyword', methods=['POST'])
def get_lecture_by_keyword():
    '''
    返回关键字对应的讲座列表
    '''
    keyword=request.form['keyword']
    
    db = pymysql.connect(mysql_path, mysql_user, mysql_pass, mysql_db)
    cursor = db.cursor()
    sql="""
    select title,organizer,introduction,field
    from lecture 
    where title like '%{}%';
    """.format(keyword)

    cursor.execute(sql)
    data=cursor.fetchall()

    lecture_list=[]

    for i in data:
        temp={}
        temp['title']=i[0]
        temp['organizer']=i[1]
        temp['introduction']=i[2]
        temp['field']=i[3]
        lecture_list.append(copy.deepcopy(temp))

    return json.dumps({'lecture_list':lecture_list},ensure_ascii=False)

# 学科页

@app.route('/subject/<subject>')
def direct_to_subject_page(subject):
    return render_template("subject_demo.html",title = subject)

# 搜索结果页

@app.route('/search=<keyword>')
def direct_to_search_result_page(keyword):
    return render_template("search_demo.html",title = keyword)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)