#贴吧小爬虫---爬取静态网页内容
import urllib
import urllib.request

class Tieba(object):
    def load_page(self,url,filename):
        """"获取网页信息"""
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
        print("正在下载%s"%filename)
        request = urllib.request.Request(url,headers=headers)
        response = urllib.request.urlopen(request)
        return response.read()

    def deal_page(self,html,filename):
        """"保存网页"""
        print("正在保存%s" % filename)
        with open(filename,"wb+") as f:
            f.write(html)
        print("成功保存%s" % filename)

    def loop(self,fullurl,pn_start,pn_end):
        """"循环获取多页网页"""
        for pn in range(pn_start,pn_end+1):
            filename = "第" + str(pn) + "页.html"
            pn = (pn - 1) * 50
            url = fullurl + str(pn)
            html = self.load_page(url,filename)
            self.deal_page(html, filename)
def main():
    tieba = Tieba()
    kw = input("请输入你要搜索的贴吧名：")
    kw = urllib.parse.urlencode({kw:"kw"})
    pn_start = int(input("请输入你要爬取的起始页："))
    pn_end = int(input("请输入你要爬取的结束页："))
    url = "http://tieba.baidu.com/f?kw="
    fullurl = url+kw+"&ie=utf-8&pn="
    tieba.loop(fullurl,pn_start,pn_end)

if __name__ == "__main__":
    main()
