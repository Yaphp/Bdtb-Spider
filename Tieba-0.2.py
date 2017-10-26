#-*coding:UTF-8*-
#author:__Yaphp__
#------贴吧图片抓取器-----
#------versi：0.1---------

import urllib
import urllib.response
import urllib.request
import re
import os
import zlib





class Tieba:
    def __init__(self,BaseUrl):
        self.BaseUrl=BaseUrl
        self.t=0
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
        response = urllib.request.urlopen(request).read().decode('utf-8')
        pattern = re.compile('red">.*?<', re.S)
        lists = re.findall(pattern, response)
        for list in lists:
                num = list.replace('red">', '')
                num1 = num.replace('<', '')
        PageNum=num1[0:2]
        return PageNum

    def getImageurl(self,response):
        #image=self.getPage()
        #pattern=re.compile('<img class="BDE_Image" src=".*?>',re.S)
        pattern = re.compile('(http://img.*?.baidu.com/forum/w%3D580/.*?.jpg|https://img.*?.baidu.com/forum/w%3D580/.*?.jpg)', re.S)
        Image=re.findall(pattern,response)
        print(Image)
        return Image

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

    def start(self,PageNum,filename):
        s=0
        for pagenum in range(1,PageNum+1):    #递增获取帖子内的页面
            Page=self.getPage(pagenum)    #保存单页里的内容
            Imageurl=self.getImageurl(Page)
            i=self.savePic(filename,Imageurl,pagenum)
            s=s+i
        print("成功写入" + str(s) + "张图片")




print("|------------------------------------------------------->")
print("|------------------ 贴吧JPG图片抓取器 --------------------->")
print("|-------------------版本号：0.2------------------------>")
print("|-------------------作者：Yaphp------------------------>")
print("|-------------------开始执行--------------------------->")

Baseurl=input("输入帖子的地址进行爬取,例如：")
see_lzNum=input("是否只看楼主，输入1是 0否")
url="https://tieba.baidu.com/p/"+Baseurl+"?see_lz="+see_lzNum
print(url)
num=Tieba(url).getPageNum()
print("该帖子总数为:"+str(num))
PageNum=int(input("请输入需要爬取的页面数:"))
filename=input("输入导出的文件夹名字")
Tieba(url).start(PageNum,filename)
input("抓取完成,按任意键退出：")