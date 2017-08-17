#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2,re

#糗百爬虫类
class QSBK:
    #初始化类，定义一些变量
    def __init__(self):
        self.page_index = 1
        #构造并初始化headers
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3103.400 QQBrowser/9.6.11372.400'
        self.headers = {'User-Agent': self.user_agent}
        #初始化一个存放段子的变量【】
        self.stories = []
        #存放程序是否运行正常的变量
        self.enable = False

    def get_page(self,page_index):
        #获取页面内容
        url = 'https://www.qiushibaike.com/hot/page/%s/' % (str(page_index))
        try:
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            page_code = response.read()
            return page_code
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print '链接糗百失败，错误原因:',e.reason
                return None

    def get_page_items(self,page_index):
        page_code = self.get_page(page_index)
        if not page_code:
            print '页面加载失败......'
            return
        pattern = re.compile(
            r'div.*?author.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<!-- 图片或gif -->(.*?)<div class="stats">.*?class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, page_code)
        page_stories = []
        for item in items:
            have_img = re.search('img',item[2])
            if not have_img:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
                #item[0]:作者；item[1]:内容;item[3]:点赞数.
                page_stories.append([item[0].strip(), text.strip(), item[3].strip()])
        return page_stories

    def load_page(self):
        if len(self.stories) < 2:
            page_stories = self.get_page_items(self.page_index)
            if page_stories:
                self.stories.append(page_stories)
                self.page_index += 1

    def get_one_story(self,page_stories,page):
        for story in page_stories:
            Input = raw_input('请输入:')
            self.load_page()
            if Input == "Q":
                self.enable = False
                return
            print "第%d页\t发布人:%s\t赞:%s\n%s" %(page,story[0],story[2],story[1])

    def start(self):
        print "正在读取糗事百科,按回车查看新段子，Q退出"
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.load_page()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.get_one_story(pageStories, nowPage)

if __name__ == '__main__':
    qb = QSBK()
    qb.start()