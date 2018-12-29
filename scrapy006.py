#开放代理和私密代理的使用
import urllib.request
import os

# 获取系统环境变量的授权代理的账户和密码
proxyuser = os.environ.get("proxyuser")
proxypasswd = os.environ.get("proxypasswd")

# 授权的代理账户密码拼接
authproxy_handler = urllib.request.ProxyHandler({"http" : proxyuser+":"+proxypasswd+"@你的代理IP:端口"})
#authproxy_handler = urllib2.ProxyHandler({"http" : "你的代理IP:端口"})

# 构建一个自定义的opener
opener = urllib.request.build_opener(authproxy_handler)

# 构建请求
request = urllib.request.Request("http://www.baidu.com/")

# 获取响应
response = opener.open(request).read()

# 打印内容
print(response)
