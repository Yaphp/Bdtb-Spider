#-*coding:UTF-8*-
#author:__Yaphp__
#------贴吧抓取器---------
#------versi：0.3--------

import requests
from bs4 import BeautifulSoup
import re
import os
import threading



#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()



class Tieba:
    def __init__(self,url):
        self.url=url
        self.zp=0
        self.tool=Tool()

    def getPage(self):#,url
        url=self.url
        r=requests.get(url)
        soup=BeautifulSoup(r.text,'html.parser')
        title_lists=soup.find_all('a','j_th_tit ')
        links=[]
        for i in title_lists:
            links.append(i.get('href'))
        #print(links)
        return links

    def get_info(self,link):
        url='http://tieba.baidu.com'+link
        r=requests.get(url)
        soup=BeautifulSoup(r.text,'html.parser')
        number=soup.find_all('span','red')[1].text
        title=soup.title.string
        return int(number),title

    def down_floor_text(self,text,i,title,n):
        path = "tieba/" + title + "/内容.txt"
        try:
            with open(path,'a') as f:
                f.write("\n------------------第"+str(n)+"楼------------------------------\n")
                f.write('\n')
                f.write(text)
                f.write('\n')
                f.write("\n-----------------------------------------------------\n\n")
        except UnicodeEncodeError:
            pass
        return


    def down_floor_img(self,imgurl,i,title,t):
        path = "tieba/" + title + "/"
        try:
            print("图片地址:"+imgurl)
            print("正在写入第 %s 页第 %s 张图片"%(i,t))
            r=requests.get(imgurl,stream=True).raw.read()
            #pic=r.read()
            with open(path+str(i)+"_"+str(t)+".jpg",'wb')as f:
                f.write(r)
                print("写入完成")
        except IOError as e:
            print(e)
            pass
        return

    def get_floor_txt(self,link,i,title,n):
        print("正在抓取本页的回复")
        url = 'http://tieba.baidu.com' + link + '?pn=' + str(i)  # list.get('href'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        all_floors = soup.find_all('div', 'd_post_content j_d_post_content  clearfix')
        for a in all_floors:
            print("正在爬取第%s楼"%(n))
            self.down_floor_text(a.text,i,title,n)
            n+=1
        print("本页回复抓取完成")
        return

    def get_floor_img(self,link,i,title,t):
        print("获取本页的图片地址")
        url = 'http://tieba.baidu.com' + link + '?pn=' + str(i)  # list.get('href'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        all_img_list = soup.find_all('img', 'BDE_Image')
        for a in all_img_list:
            #print(a.attrs['src'])
            url=a.attrs['src']
            self.down_floor_img(url,i,title,t)
            t=t+1
        print("本页图片下载完成")
        return



    def get_floors(self,link):
        try:
            page_num = self.get_info(link)[0]
            title = self.get_info(link)[1]
            path = "tieba/" + title
            isExists = os.path.exists(path)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                try:
                    os.makedirs(path)
                except IOError:
                    pass
            else:
                # 如果目录存在则不创建，并提示目录已存在
                print("目录已存在")
                return

            print("正在爬取帖子：" + title)
            print("该帖子总共有:" + str(page_num) + "页")
            n=1
            t=1
            for i in range(1,page_num+1):
                print("正在抓取第 %s 页"%(i))
                threading._start_new_thread(self.get_floor_txt,(link,i,title,n))
                threading._start_new_thread(self.get_floor_img,(link,i,title,t))
                print("第 %s 页抓取完成"%(i))
                print('\n')
            print(title+"爬取完成"+'\n\n')

        except IOError as e:

            print("出现错误，原因如下:"+e.errno)





    def start_go(self):
        try:
            while True:
                self.url=self.url+str(self.zp)
                links=self.getPage()
                for link in links:
                    self.get_floors(link)
                self.zp+=50

        except IOError as e:
            print("哎呀出错了")
            print(e.errno)






print("|------------------------------------------------------>")
print("|------------------ 贴吧抓取器 ------------------------->")
print("|-------------------版本号：0.4------------------------->")
print("|-------------------作者：Yaphp------------------------->")
print("|-------------------开始执行---------------------------->")


# Baseurl=input("输入帖子的地址进行爬取,例如：5093826937")
# see_lzNum=input("是否只看楼主，输入1是 0否")
# url="https://tieba.baidu.com/p/"+Baseurl+"?see_lz="+see_lzNum
# num=Tieba(url).getPageNum()
# print("该帖子总数为:"+str(num))
# PageNum=int(input("请输入需要爬取的页面数:"))
# filename=input("输入导出的文件夹名字")
# Tieba(url).start(PageNum,filename)
# input("抓取完成,按任意键退出：")
#Tieba(url).getPage()

print("输入tieba的地址进行爬取,例如：http://tieba.baidu.com/f?kw=苍溪实验中学")
tiebaurl=str(input("请输入："))
url=tiebaurl+'&ie=utf-8&pn='
Tieba(url).start_go()