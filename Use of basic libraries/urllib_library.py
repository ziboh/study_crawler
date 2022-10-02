import http.cookiejar
from urllib.error import HTTPError, URLError
import urllib.request
import urllib.parse

# 使用urlopen发送get请求
"""
response = urllib.request.urlopen("https://python.org")
print(type(response))
print(response.__dict__)
print(response.status)
print(response.getheaders())
print(response.getheader("server"))
print(response.read().decode("utf-8"))
"""

# 使用urlopen发送post请求
"""
data = bytes(urllib.parse.urlencode({"name":"zibo"}),encoding="utf-8")
response_post = urllib.request.urlopen("https://httpbin.org/post",data=data)
print(response_post.read().decode("utf-8"))
"""


# 设置timeout
"""
try:
    response_timeout = urllib.request.urlopen("https://httpbin.org/get",timeout=1)
    print(response_timeout.read().decode("utf-8"))
except urllib.error.URLError:
    print("timeout")
"""


# Request使用
"""
request = urllib.request.Request("https://python.org")
response = urllib.request.urlopen(request)
print(response.read().decode("utf-8"))
"""


# 使用Request类构建对象
"""
url = "https://www.httpbin.org/post"
headers = {
    "User-Agent":"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
    "Host": "www.httpbin.org"
}
data = bytes(urllib.parse.urlencode({"name":"zibo"}),encoding="utf-8")
req = urllib.request.Request(url=url,headers=headers,data=data,method="POST")
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
"""


# 使用Handler类进行高级用法
# 密码验证

"""
from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener
from urllib.error import URLError

username = "admin"
password = "admin"
url= "https://ssr3.scrape.center/"

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None,url,user=username,passwd=password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
    response = opener.open(url)
    print(response.read().decode("utf-8"))
except URLError as e:
    print(e.reason)
"""
# 使用代理
"""
from urllib.error import URLError

proxy_handler = ProxyHandler(
    {
        "http": "http://192.168.1.2:7893",
        "https": "https://192.168.1.2:7893"
    }
)

opener = build_opener(proxy_handler)

try:
    response =opener.open("https://google.com/")
    print(response.read().decode("utf-8"))
except URLError as e:
    print(e.reason)
"""
# 获取Cookie

"""
OpenerDirector = urllib.request.OpenerDirector
cookie: http.cookiejar.CookieJar = http.cookiejar.CookieJar()
handler: urllib.request.HTTPCookieProcessor = urllib.request.HTTPCookieProcessor(
    cookie)
opener: OpenerDirector = urllib.request.build_opener(handler)
response = opener.open("https://www.baidu.com")
for item in cookie:
    print(item.name + "=" + item.value)
"""
# 以Mozilla浏览器格式保存cookie

"""
filename = "cookie.txt"
cookie= http.cookiejar.MozillaCookieJar(filename)
handler= urllib.request.HTTPCookieProcessor(
    cookie)
opener= urllib.request.build_opener(handler)
response = opener.open("https://www.baidu.com")
cookie.save()
for item in cookie:
    print(item.name + "=" + item.value)
"""
# 以LWP格式保存cookie

"""
filename = "cookie_lwp.txt"
cookie= http.cookiejar.LWPCookieJar(filename)
handler= urllib.request.HTTPCookieProcessor(
    cookie)
opener= urllib.request.build_opener(handler)
response = opener.open("https://www.baidu.com")
cookie.save()
for item in cookie:
    print(item.name + "=" + item.value)

"""
# 异常捕获URLError
"""

try:
    response = urllib.request.urlopen("https://cuiqingcai.com/404")
except URLError as e:
    print(e.reason)
    
"""
# 异常捕获HTTPError(为URLError的子类)
"""


try:
    response = urllib.request.urlopen("https://cuiqingcai.com/404")
except HTTPError as e:
    print("HTTPerror",end=":")
    print(e.reason)

except URLError as e:
    print("URLerror",e.reason,sep=":")    
else:
    print("Request successfully")

"""
# urllib.parse.urlparse的使用
"""
result = urllib.parse.urlparse("https://kaifa.baidu.com/searchPage?wd=mypy%E9%94%99%E8%AF%AF%E6%A3%80%E6%B5%8B",allow_fragments=False)
print(result)


"""
# urllib.parse.urlunparse的使用
# urlunparse参数为iterable object , object's length is six
"""
result = urllib.parse.urlunparse(["https","baidu.com","index.html","user","a=6","coment"])
print(result)

"""
# urllib.parse.urlsplit的使用
"""
result = urllib.parse.urlsplit("https://kaifa.baidu.com/searchPage?wd=mypy%E9%94%99%E8%AF%AF%E6%A3%80%E6%B5%8B",allow_fragments=False)
print(result)

"""
# urllib.parse.urlunsplit的使用
# urlunsplit参数为iterable object , object's length is five
"""
result = urllib.parse.urlunsplit(
    ["https", "baidu.com", "index.html", "a=6", "coment"])
print(result)

"""

# urlencode 将字典转成GET请求参数形式的字符串
"""
from urllib.parse import urlencode

params = {
    "name":"zibo",
    "age":"18"
}

url = "https://www.baidu.com/index.html?" + urlencode(params)
print(url)
"""
# parse_qs 将GET请求参数形式的字符串转成字典
"""
query = "name=zibo&age=18"
result = urllib.parse.parse_qs(query)
print(result)
"""
# parse_qsl 将GET请求参数形式的字符串转成由tuple 组成的列表
"""
query = "name=zibo&age=18"
result = urllib.parse.parse_qsl(query)
print(result)
"""
# quote 将内容转成URL编码格式
"""
keyword = "壁纸"
url = "https://www.baidu.com/s?wd=" +  urllib.parse.quote(keyword)
print(url)

"""
# unquote URL编码格式转成对应内容
"""
url = "https://www.baidu.com/s?wd=%E5%A3%81%E7%BA%B8"
print(urllib.parse.unquote(url))

"""
# robots协议
# robotparser
"""
from urllib.robotparser import RobotFileParser
rp = RobotFileParser()
rp.set_url("https://www.baidu.com/robots.txt")
rp.read()
print(rp.can_fetch("Baiduspider","https://www.baidu.com"))
print(rp.can_fetch("Baiduspider","https://www.baidu.com/homepage/"))
print(rp.can_fetch("Googlebot","https://www.baidu.com"))
print(rp.can_fetch("Googlebot","https://www.baidu.com/homepage/"))
"""
