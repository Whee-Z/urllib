#爬糗事百科小案例

#网页链接：https://www.qiushibaike.com/8hr/page/1/
#帖子链接：https://www.qiushibaike.com + //div/a[@class="recmd-content"]/@href
#帖子好笑数：//div/span/i[@class="number"]/text()
#帖子内容：//div/a[@class="recmd-content"]/text()
#帖子图片：//div[@class="thumb"]/img/@src
#帖子视频：//div/video[@id="article-video"]/source/@src

import urllib.request
from lxml import etree

class Qiushi(object):
    """"爬取糗事百科帖子内容、图片、视频、点赞数和评论数"""
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    def load_page(self,url):
        """"获取糗事百科网页内容"""
        request = urllib.request.Request(url,headers=self.headers)
        response = urllib.request.urlopen(request).read()
        self.deal_page(response)

    def deal_page(self,html):
        """"获取每条帖子的链接"""
        html = etree.HTML(html)
        link_list = html.xpath('//div/a[@class="recmd-content"]/@href')

        for link in link_list:
            tiezi_url = "https://www.qiushibaike.com" + link
            #print(tiezi_url)
            self.deal_content(tiezi_url)

    def deal_content(self,url):
        """"处理获得的帖子链接，找到帖子内容、图片、视频、点赞数和评论数"""
        request = urllib.request.Request(url,headers=self.headers)
        response = urllib.request.urlopen(request).read()
        html = etree.HTML(response)
        zan = html.xpath('//div/span/i[@class="number"]/text()')
        #print(zan)
        tiezi_content = html.xpath('//div/h1/text()')
        #print(tiezi_content)
        tiezi_pic = html.xpath('//div[@class="thumb"]/img/@src')
        #print(tiezi_pic)
        tiezi_video = html.xpath('//div/video[@id="article-video"]/source/@src')
        #print(tiezi_video)
        items = {
            "帖子内容":tiezi_content,
            "帖子赞数":zan,
            "帖子图片":tiezi_pic,
            "帖子视频":tiezi_video
        }
        #print(items)
        self.write_content(items)

    def write_content(self,items):
        """"将获取的信息写入txt文件"""
        with open('qiushi.txt','a',encoding='utf-8') as f:
            f.write(str(items)+'\n')

    def controller(self,page_begin,page_end):
        """"程序控制器"""
        print("请稍等")
        for pg in range(page_begin,page_end+1):
            url = "https://www.qiushibaike.com/8hr/page/"
            print("正在写入第%s页"%pg)
            url = url + str(pg) + '/'
            #print(url)
            with open("qiushi.txt","a") as f:
                f.write('page' + str(pg) + '\n')
            self.load_page(url)
            print("成功写入第%s页"%pg)
        print("已全部写入")

def main():
    qiushi = Qiushi()
    page_begin = int(input("请输入你想爬的起始页："))
    page_end = int(input("请输入你想爬的结束页："))
    qiushi.controller(page_begin,page_end)

if __name__ == '__main__':
    main()


