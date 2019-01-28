#爬糗事百科小案例---多线程

#网页链接：https://www.qiushibaike.com/8hr/page/1/
#帖子链接：https://www.qiushibaike.com + //div/a[@class="recmd-content"]/@href
#帖子好笑数：//div/span/i[@class="number"]/text()
#帖子内容：//div/a[@class="recmd-content"]/text()
#帖子图片：//div[@class="thumb"]/img/@src
#帖子视频：//div/video[@id="article-video"]/source/@src

from lxml import etree
import threading
import requests
from queue import Queue
import json
import time

class ThreadCrawl(threading.Thread):
    """"网页采集线程"""
    def __init__(self,thread_name,page_queue,data_queue):
        #调用父类初始化方法
        super(ThreadCrawl,self).__init__()
        #线程名
        self.thread_name = thread_name
        #页面采集队列
        self.page_queue = page_queue
        #数据采集队列
        self.data_queue = data_queue
        #请求报头
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        self.controller()

    def load_page(self, url):
        """"获取糗事百科网页内容"""
        response = requests.get(url, headers=self.headers).text
        self.deal_page(response)

    def deal_page(self, html):
        """"获取每条帖子的链接"""
        html = etree.HTML(html)
        link_list = html.xpath('//div/a[@class="recmd-content"]/@href')

        for link in link_list:
            tiezi_url = "https://www.qiushibaike.com" + link
            print(tiezi_url)
            self.data_queue.put(tiezi_url)
            #time.sleep(1)


    def controller(self):
        """"程序控制器"""
        print("启动"+self.thread_name)
        while not CRAWLEXIT:
            try:
                pg = self.page_queue.get(False)
                url = "https://www.qiushibaike.com/8hr/page/"+ str(pg) + '/'
                print("正在写入第%s页"%pg)
                print(url)
                #with open("qiushi.json","a") as f:
                    #f.write('page' + str(pg) + '\n')
                self.load_page(url)
            except:
                break

        print("结束"+self.thread_name)

class ThreadParse(threading.Thread):
    """"数据采集线程"""
    def __init__(self,parse_name,lock,filename):
        super(ThreadParse, self).__init__()
        self.lock = lock
        self.filename = filename
        self.parse_name = parse_name
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    def deal_content(self,url):
        """"处理获得的帖子链接，找到帖子内容、图片、视频、点赞数和评论数"""
        print(url)
        response = requests.get(url,headers=self.headers).text
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
        # with 后面有两个必须执行的操作：__enter__ 和 _exit__
        # 不管里面的操作结果如何，都会执行打开、关闭
        # 打开锁、处理内容、释放锁
        with self.lock:
            # 写入存储的解析后的数据
            self.write_content(items)

    def write_content(self,items):
        """"将获取的信息写入txt文件"""
        print(items)
        self.filename.write(str(json.dumps(items, ensure_ascii = False)) + "\n")


    def controller(self,data_queue):
        """"程序控制器"""
        print("启动"+self.parse_name)
        while not PARSEEIXT:
            try:
                html = data_queue.get(False)
                #time.sleep(1)
                self.deal_content(html)
                #print("成功写入第%s页"%pg)
                print("已写入")
            except:
                break

        print("结束"+self.parse_name)

CRAWLEXIT = False
PARSEEIXT = False

def main():
    #创建页面队列
    page_queue = Queue()
    #将1-10放入页面队列，先进先出
    for i in range(1,8):
        page_queue.put(i)
    #创建采集到源码的数据队列
    data_queue = Queue()
    filename = open("qiushi.json","a")
    #创建锁
    lock = threading.Lock()
    #采集线程
    crawl_list = ["采集线程1号","采集线程2号","采集线程3号"]
    #新建一个列表保存采集线程
    thread_crawl = []
    for thread_name in crawl_list:
        thread = ThreadCrawl(thread_name,page_queue,data_queue)
        thread.start()
        thread_crawl.append(thread)

    #解析线程
    parse_list = ["解析线程1号","解析线程2号","解析线程3号","解析线程4号","解析线程5号","解析线程6号","解析线程7号","解析线程8号"]
    #新建一个列表保存解析线程
    thread_parse = []
    for parse_name in parse_list:
        thread = ThreadParse(parse_name,lock,filename)
        thread.controller(data_queue)
        thread.start()
        thread_parse.append(thread)

    #等待page_queue为空然后继续往下执行
    while not page_queue.empty():
        pass

    #若队列为空，结束采集线程

    #global CRAWLEXIT
    #CRAWLEXIT = True
    print("采集队列已空")

    for thread in thread_crawl:
        thread.join()
        #print("1")

    while not data_queue.empty():
        pass

    #global PARSEEXIT
    #PARSEEXIT = True
    print("数据队列已空")

    for thread in thread_parse:
        thread.join()
        #print("2")

    with lock:
        filename.close()
    print("数据已全部写入")

if __name__ == '__main__':
    main()


