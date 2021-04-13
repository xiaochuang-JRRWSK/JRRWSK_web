import pymysql

subtitle={"journalism":"新闻传播","engineering":"计算机",
"art":"艺术","history":"历史","literature":"文学",
"engineering":"工学","natural":"自然科学","economics":"经济学",
"education":"教育学","management":"工商管理","communication":"传播学",
"philosophy":"哲学","law":"法学"}

class Text:
    '''根据数据库内讲座数据生成讲座介绍'''

    def __init__(self,id):
        self.id = id
        self.my_dict = {'id':id,
                        'title':"",
                        'keyword':"",
                        'person':"",
                        'time':"",
                        'location':"",
                        'lecture_intro':"",
                        'person_intro':"",
                        'total_intro':"",
                        'organizer':"",
                        'source':"",
                        'total_content':""}

    def db_connect(self):
        #连接数据库

        mysql_path="82.156.28.161"
        mysql_user="mysql"
        mysql_pass="xiaochuang12345"
        mysql_db="xiaochuang"

        self.db = pymysql.connect(host=mysql_path,user=mysql_user,passwd=mysql_pass,db=mysql_db)
        self.cursor = self.db.cursor()
    
    def get_lecture_info(self):
        #获取讲座信息
        sql="""
            select title,organizer,starttime,overtime,location,field,introduction,articleID
            from lecture 
            where ID = '{}';
            """.format(self.id)

        self.cursor.execute(sql)
        data=self.cursor.fetchall()

        try:
            self.title = data[0][0]
            self.organizer = data[0][1]
            self.start_time = str(data[0][2])[:-3]
            self.over_time = str(data[0][3])[:-3]
            self.location = data[0][4]
            self.field = data[0][5]
            self.original_introduction = data[0][6]
            self.articleID = data[0][7]

        except IndexError:
            #print("讲座id失效")
            self.title = ""
            self.organizer = ""
            self.start_time = ""
            self.over_time = ""
            self.location = ""
            self.field = ""
            self.original_introduction = ""
            self.articleID = -1

        print("articleID:",self.articleID)

    def get_person_info(self):
        #获取讲座人信息
        if (self.articleID != -1):
            sql="""
            select name,information,achievement,field
            from people 
            where articleID = '{}';
            """.format(self.articleID)

            self.cursor.execute(sql)
            data=self.cursor.fetchall()
        
            try:
                self.person_name = data[0][0]
                self.person_infos = data[0][1]
                self.person_achievement = data[0][2]
                self.person_field = data[0][3]
            except IndexError:
                #print("讲座人数据缺失")
                self.person_name = ""
                self.person_infos = ""
                self.person_achievement = ""
                self.person_field = ""
        else:
                self.person_name = ""
                self.person_infos = ""
                self.person_achievement = ""
                self.person_field = ""


    
    def get_source_info(self):
        #获取数据来源信息
        if(self.articleID != -1):
            sql="""select link from article where ID = '{}';""".format(self.articleID)

            self.cursor.execute(sql)
            self.source =str(self.cursor.fetchone()[0])
        else:
            self.source = ""
        

    def lecture_introduction_generate(self):
        #讲座内容介绍生成
        txt = ""
        if(len(self.original_introduction)>5):
            txt += self.original_introduction
        else:
            txt = str(self.start_time)+"由"+self.person_name+"主讲,以"+self.title+"为主题的讲座将在"+self.location+"举办。"
        
        self.my_dict['lecture_intro'] = txt
        return txt

    def person_introduction_generate(self):
        #讲座人介绍生成
        txt = self.person_name
        if(len(self.person_field)>5):
            txt = txt + "<br>研究方向："+self.person_field
        if(len(self.person_infos)>5):
            txt = txt + "<br>个人经历："+self.person_infos
        if(len(self.person_achievement)>5):
            txt = txt + "<br>获得成就："+self.person_achievement

        self.my_dict['person_intro'] = txt
        return txt
        
    def introduction_generate(self):
        #讲座内容介绍生成函数，对于讲座内容介绍缺省的讲座，采用讲座人介绍
        self.introduction = ""

        lecture_introduction = self.lecture_introduction_generate()
        person_intorduction = self.person_introduction_generate()

        if(len(lecture_introduction)+len(person_intorduction)<5):
            self.introduction = "【讲座介绍】：暂无。<br>"
        if(len(lecture_introduction) >= 5):
            self.introduction = "【讲座介绍】"+lecture_introduction+"<br>"
        if(len(person_intorduction) >= 5):
            self.introduction = self.introduction + "【讲座人介绍】"+person_intorduction

        self.my_dict['total_intro'] = self.introduction

    def text_combine(self):
        #完整文本拼接函数
        if(self.articleID!=-1):
            txt=""
            #讲座主题
            # txt = "【讲座主题】"+self.title
            self.my_dict['title'] = self.title
        
            #讲座人
            if(len(self.person_name)>1):
                txt += "【讲座人】"+self.person_name+"<br>"
                self.my_dict['person'] = self.person_name
        
            #讲座时间
            if(len(self.over_time)<4):
                txt += "【时间】"+self.start_time
                self.my_dict['time'] = self.start_time
            else:
                txt += "【时间】"+self.start_time+"--"+self.over_time[-5:]
                self.my_dict['time'] = self.start_time+"--"+self.over_time[-5:]
        
            #讲座地点
            txt += "<br>【地点】"+self.location+"<br>"+self.introduction
            self.my_dict['location'] = self.location

            #主办方
            if (len(self.organizer)>3):
                txt += "<br>【主办方】"+self.organizer
                self.my_dict['organizer'] = self.organizer

            #数据来源    
            txt += "<br><br>数据来源：<a href="+self.source+" >"+self.source+"</a>"
            self.my_dict['source'] = self.source

            #关键词
            txt += "<br><br>学科关键词："+subtitle[self.field]
            self.my_dict['keyword'] = subtitle[self.field]
        
        else:
            txt = "无数据"
        # print(txt)
        return txt

    def func(self):
        #文本生成模块流程函数
        self.db_connect()
        self.get_lecture_info()
        self.get_person_info()
        self.get_source_info()
        self.introduction_generate()
        self.my_dict['total_content'] = self.text_combine()


def main(ID):
    lecture_id = ID  # 传入参数为讲座id，有效数据范围为1-1140

    my_text = Text(lecture_id)
    my_text.func()
    
    print(my_text.my_dict)
    return my_text.my_dict  # 返回值为讲座介绍文本

if __name__ == "__main__":
    ID=input("请输入讲座id：")
    main(ID)