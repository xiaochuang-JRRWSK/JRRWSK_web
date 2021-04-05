from flask import Flask, request, render_template, jsonify
from flask_cors import *
import time
import pymysql
import json
import copy

app = Flask(__name__)


mysql_path="82.156.28.161"
mysql_user="mysql"
mysql_pass="xiaochuang12345"
mysql_db="xiaochuang"
ip="localhost"


@app.route('/search=<keyword>')

def index(keyword):
    db = pymysql.connect(host=mysql_path, 
                        user=mysql_user, 
                        passwd=mysql_pass, 
                        db=mysql_db)
    cursor = db.cursor()
    sql="""
    select title,organizer,introduction,field
    from lecture 
    where title like '%{}%';
    """.format(keyword)

    cursor.execute(sql)
    data=cursor.fetchall()

    result_list=[]
    
    for i in data:         
        temp={}
        temp['title']=i[0]
        temp['organizer']=i[1]
        temp['introduction']=i[2]
        temp['field']=i[3]
        result_list.append(copy.deepcopy(temp))

    db.close()
    
    result = result_list[0]
    title = result['title']
    length = len(result_list)
    
    content = text_module(result)
    return render_template('search_demo.html',
                            keyword = keyword,
                            title = title,
                            content = content,
                            length = length,
                            result_list = result_list)

#文本生成接口，待扩展
def text_module(result):
    content = "讲座名称:"+result['title']+"\n组织者:"+result['organizer']+"\n简介："+result['introduction']
    return content

if __name__ == '__main__':
    app.run(debug=True)