#贴吧小爬虫案例

import urllib
#python2中import urllib2
import urllib.request

def load_page(url,filename):
    """"
    作用：根据url发送请求，获取服务器响应文件
    url:需要爬取的url地址
    filrname:正在下载的文件名
    """
    print("正在下载%s"%filename)
    headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    request = urllib.request.Request(url,headers=headers)
    return urllib.request.urlopen(request).read()


def write_page(html,filename):
    """"
    作用：将html写入本地
    html：服务器相应文件内容
    """
    print("正在保存%s" % filename)

    #写入文件
    with open(filename,'wb+') as f:
        f.write(html)

    print("成功保存%s" % filename)
    print("----------------------")

def tieba_spider(url,start_page,end_page):
    """"
    作用：贴吧爬虫调度器，负责组合处理每个页面的url
    url:贴吧url的前部分
    start_page:起始页
    end_page:结束页
    """
    for page in range(start_page,end_page+1):
        pn = (page-1) * 50
        filename = '第' + str(page) +'页.html'
        fullurl = url + "&pn=" +str(pn)
        #print("%s"%fullurl)
        html = load_page(fullurl,filename)
        #print("%s"%html)
        write_page(html,filename)

def main():
    kw = input("请输入你要爬取的贴吧名：")
    start_page = int(input("请输入爬取的起始页："))
    end_page = int(input("请输入爬取的结束页："))
    url = "http://tieba.baidu.com/f?"
    #python2中用urllib.urlencode
    key = urllib.parse.urlencode({"kw":kw})
    fullurl = url + key
    tieba_spider(fullurl,start_page,end_page)

if __name__ == '__main__':
    main()