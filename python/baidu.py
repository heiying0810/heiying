#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2,re

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

class BDTB:
    def __init__(self,baseurl,seeLZ,floor_tag):
        #初始化相关参数
        self.baseurl = baseurl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.default_title = '百度贴吧'
        self.floor_tag = floor_tag

    def get_page(self,page_num):
        #获取帖子内容
        try:
            url = self.baseurl + self.seeLZ + '&pn=' + str(page_num)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print '连接百度贴吧失败，错误原因:',e.reason
                exit()

    def get_title_pagenum(self,page):
        #获取帖子标题和页数
        pattern_title = re.compile(r'<h3 class="core_title_txt pull-left text-overflow  " title="(.*?)".*?</h3>',re.S)
        pattern_num = re.compile(r'<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result_title,result_num = re.search(pattern_title,page),re.search(pattern_num,page)
        if result_title or result_num:
            return result_title.group(1).strip(),result_num.group(1).strip()
        else:
            return

    def get_content(self,page):
        #获取贴吧每一页的内容
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            content = '\n' + self.tool.replace(item) + '\n'
            contents.append(content)
        return contents

    def set_file_title(self,title):
        #新建文本文件
        if title is not None:
            self.file = open(title.decode('utf-8') + '.txt','w+')
        else:
            self.file = open(self.default_title.decode('utf-8') + '.txt' + 'w+')

    def write_data(self,contents):
        #将数据写入文件
        for item in contents:
            if self.floor_tag == '1':
                # 楼之间的分隔符
                floorLine = "\n" + str(self.floor) + '*' * 50 + '\n'
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.get_page(1)
        pageNum = self.get_title_pagenum(indexPage)[1]
        title = self.get_title_pagenum(indexPage)[0]
        self.set_file_title(title)
        if pageNum == None:
            print "URL已失效，请重试"
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1, int(pageNum) + 1):
                print "正在写入第" + str(i) + "页数据"
                page = self.get_page(i)
                contents = self.get_content(page)
                self.write_data(contents)
        # 出现写入异常
        except IOError, e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"

if __name__ == "__main__":
    baseURL = 'http://tieba.baidu.com/p/' + str(raw_input('请输入帖子代号:'))
    seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
    floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
    bdtb = BDTB(baseURL, seeLZ, floorTag)
    bdtb.start()