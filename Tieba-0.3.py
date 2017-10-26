#-*coding:UTF-8*-
#author:__Yaphp__
#------贴吧抓取器---------
#------versi：0.3--------

import urllib
import urllib.response
import urllib.request
import re
import os




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
    def __init__(self,BaseUrl):
        self.BaseUrl=BaseUrl
        self.t=0
        self.tool=Tool()

    def getPage(self,pagenum):
        url=self.BaseUrl+"&pn="+str(pagenum)
        print(url)
        request=urllib.request.Request(url)
        response = urllib.request.urlopen(request).read().decode('utf-8')
        print("正在爬取第"+str(pagenum)+"页......")
        return response

    def getPageNum(self):
        url = self.BaseUrl
        request = urllib.request.Request(url)
        #sdf=urllib.request.urlopen(request)
        #print(sdf.info())获取网页信息判断编码及是否压缩传输
        response = urllib.request.urlopen(request).read().decode('utf-8')
        pattern = re.compile('red">.*?<', re.S)
        lists = re.findall(pattern, response)
        for list in lists:
                num = list.replace('red">', '')
                num1 = num.replace('<', '')
        PageNum=num1[1:2]
        return PageNum

    def getImageurl(self,response):
        #image=self.getPage()
        #pattern=re.compile('<img class="BDE_Image" src=".*?>',re.S)
        pattern = re.compile('https://imgsa.baidu.com/forum/w%3D580/.*?.jpg', re.S)
        Image=re.findall(pattern,response)
        return Image

    def getTitle(self,response):
        pattern = re.compile('<title>.*?</title>', re.S)
        Title = re.findall(pattern, response)
        for title in Title:
            one=title.replace('<title>','')
            T=one.replace('</title>','')
        return T

    def getContent(self,page):
        #匹配所有楼层的内容
        pattern = re.compile('class="d_post_content j_d_post_content ">(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            #将文本进行去除标签处理，同时在前后加入换行符
            contents = '\n'+self.tool.replace(item)+'\n'
            #contents.append(content.encode('utf-8'))
        return contents

    def savePic(self,filename,Image,pagenum):
        #urls=self.getImageurl()
        path = "Picture/"+ filename + "/"+str(pagenum)+"/"
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print("正在创建文件夹,目录地址为："+path)
            os.makedirs(path)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print("目录已存在")
        #print(urls)
        i = 0
        for url in Image:
            i = i + 1
            #date=time.strftime("%H%M%S%f", time.localtime())
            request = urllib.request.Request(url)
            pics = urllib.request.urlopen(request).read()
            out = open("Picture/" + filename + "/"+str(pagenum)+"/" + str(i) + ".jpg", 'wb')
            out.write(pics)
            print("正在写入第" + str(i) + "张图片....")
            out.close()
        print("写入完成！第"+str(pagenum)+"页一共写入图片" + str(i) + "张")
        return i

    def saveContent(self,filename,pagenum,C):
        path = "Picture/" + filename + "/" + str(pagenum) + "/"
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print("正在创建文件夹,目录地址为：" + path)
            os.makedirs(path)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print("目录已存在")
        i=0
        out = open("Picture/" + filename + "/" + str(pagenum) + "/tiezi.txt", 'w')

        out.write("第"+str(i)+"层---------------------")
        out.write(C)
        out.close()
        print("写入完成！")
        return

    def start(self,PageNum,filename):
        for pagenum in range(1, PageNum + 1):  # 递增获取帖子内的页面
            Page = self.getPage(pagenum)  # 保存单页里的内容
            T=self.getTitle(Page)
            C=self.getContent(Page)
            self.saveContent(filename,pagenum,C)
        print("成功写入")





print("|------------------------------------------------------>")
print("|------------------ 贴吧抓取器 ------------------------->")
print("|-------------------版本号：0.2------------------------->")
print("|-------------------作者：Yaphp------------------------->")
print("|-------------------开始执行---------------------------->")


Baseurl=input("输入帖子的地址进行爬取,例如：5093826937")
see_lzNum=input("是否只看楼主，输入1是 0否")
url="https://tieba.baidu.com/p/"+Baseurl+"?see_lz="+see_lzNum
num=Tieba(url).getPageNum()
print("该帖子总数为:"+str(num))
PageNum=int(input("请输入需要爬取的页面数:"))
filename=input("输入导出的文件夹名字")
Tieba(url).start(PageNum,filename)
input("抓取完成,按任意键退出：")

