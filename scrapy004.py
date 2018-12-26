#获取豆瓣电影排行ajax页面数据
import urllib
import urllib.request
import json


url = "https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action"

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

formdata = {
        "start":"0",
        "limit":"20"
    }
#加encode("utf8")是保证输出是str，但输出是十六进制
data = urllib.parse.urlencode(formdata).encode("utf8")

request = urllib.request.Request(url, data = data, headers = headers)

result = urllib.request.urlopen(request).read()

#导入json模块为的就是输出来是中文
print("%s"%(json.dumps(json.loads(result),ensure_ascii=False)))