#爬百度某贴吧帖子的图片小案例

import urllib
import urllib.request
from lxml import etree

class TiebaPic(object):
    """"获取贴吧中帖子的图片"""
    def __init__(self):
        self.headers = headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    def load_page(self,url):
        """"获取贴吧页面"""
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request).read()
        self.deal_page(response)

    def deal_page(self,response):
        """"h获取帖子的链接"""
        html = etree.HTML(response)
        page_link = html.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        for link in page_link:
            page_url = "http://tieba.baidu.com" + link
            #print(page_url)
            self.deal_pic(page_url)


    def deal_pic(self,page_url):
        """"获取帖子中的图片"""
        request = urllib.request.Request(page_url,headers=self.headers)
        response = urllib.request.urlopen(request).read()
        html = etree.HTML(response)
        pic_link = html.xpath('//cc/div/img[@class="BDE_Image"]/@src')
        for pic_url in pic_link:
            self.write_pic(pic_url)

    def write_pic(self,pic_url):
        """"将图片保存到本地"""
        request = urllib.request.Request(pic_url,headers=self.headers)
        response = urllib.request.urlopen(request).read()
        filename = pic_url[-8:]
        with open(filename,"wb") as f:
            f.write(response)
            print("正在下载%s"%filename)

    def controller(self,url,page_start,page_end):
        """"逐页获取图片"""
        for pn in range(page_start,page_end+1):
            pn = (pn-1)*50
            url = url + "&ie=utf-8&pn=" + str(pn)
            self.load_page(url)
        print("已全部下载完成")

def main():
    tiebaPic = TiebaPic()
    kw = input("请输入你要爬取图片的贴吧名：")
    page_start = int(input("请输入你要爬取图片的贴吧起始页："))
    page_end = int(input("请输入你要爬取图片的贴吧结束页："))
    kw = urllib.parse.urlencode({"kw":kw})
    url = "http://tieba.baidu.com/f?"
    fullurl = url + kw
    print(fullurl)
    tiebaPic.controller(fullurl,page_start,page_end)

if __name__ == "__main__":
    main()
