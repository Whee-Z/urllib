#获取百度一下的网页内容
import urllib.request

u_headers = {"User-Agent":"Mozilla/5.0(win)"}
#构造一个请求对象
request = urllib.request.Request("http://www.baidu.com",headers = u_headers)

#向指定的url地址发送请求，并返回服务器的类文件对象
response = urllib.request.urlopen(request)

#服务器返回的类文件对象支持python文件对象的操作方法
#read（）的方法就是读取文件的全部内容，返回字符串
html = response.read()

print("%s"%html)