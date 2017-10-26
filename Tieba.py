#-*coding:utf-8*_
#author:__Yaphp__
#------贴吧图片抓取器-----
#------versi：0.1---------

import urllib
import urllib.response
import urllib.request
import re
import sys
import time
import os





class Tieba:
    def __init__(self,BaseUrl):
        self.BaseUrl=BaseUrl



    def getPage(self):
        url=self.BaseUrl
        request=urllib.request.Request(url)
        response=urllib.request.urlopen(request).read().decode('utf-8')
        return response

    def getImageurl(self):
        image=self.getPage()
        #pattern=re.compile('<img class="BDE_Image" src=".*?>',re.S)
        pattern = re.compile('https://imgsa.baidu.com/forum/w%3D580/.*?.jpg', re.S)
        Image=re.findall(pattern,image)
        return Image

    def saveUrl(self):
        image=self.getImageurl()
        out = open("PicUrl/url.txt", 'w')
        for imageurl in image:
            try:
                imageURL=imageurl.replace('<img class="BDE_Image" src="','')
                out.write(imageURL+'\n')
            except IOError as e:
                print("写入失败")
        out.close()

    def savePic(self,filename):
        urls=self.getImageurl()
        path = "Pic/" + filename + "/"
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
        for url in urls:
            i = i + 1
            date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            request = urllib.request.Request(url)
            pics = urllib.request.urlopen(request).read()
            out = open("Pic/" + filename + "/" + str(i) + ".jpg", 'wb')
            out.write(pics)
            print("正在写入第" + str(i) + "张图片....")
            out.close()
        print("写入完成！一共写入图片" + str(i) + "张")




print("-----------------------------------------------------")
print("-------------------贴吧图片抓取器---------------------")
print("-------------------版本号：0.1------------------------")
print("-------------------开始执行---------------------------")
url=input("输入帖子的某一页的地址进行爬取")
filename=input("输入导入的文件夹名字")
Tieba(url).savePic(filename)