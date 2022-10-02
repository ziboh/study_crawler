import requests
import urllib

# 直接使用get,post,put,delete方法即可
"""

r = requests.get("https://www.baidu.com")
print(r.cookies)
print(r.status_code)
# print(r.text)
print(r.text[:100])
r_get = requests.get("https://www.httpbin.org/get")
r_post = requests.post("https://www.httpbin.org/post")
r_put = requests.put("https://www.httpbin.org/put")
r_delete = requests.delete("https://www.httpbin.org/delete")
r_patch = requests.patch("https://www.httpbin.org/patch")


print(r_get.text,r_post.text,r_put.text,r_delete.text,r_patch.text,sep="\n")
"""
#  requests.get的使用

"""
r_get = requests.get("https://www.httpbin.org/get?name=zibo&age=18")
# print(r_get.text)
r_get_params = requests.get("https://www.httpbin.org/get",params={"name":"zibo","age":18})
print(r_get_params.text)
print(r_get_params.json())
"""


# cookie 设置
"""
cookies = "_octo=GH1.1.2120769424.1657936314; logged_in=yes; _device_id=ad9d72ff6db953c3a5f91fbdd7f97eda; user_session=kAN4-sVls7M3GD9mWJeQBgz_UPGXSyOqWPNnH3hARKg4KGB-; __Host-user_session_same_site=kAN4-sVls7M3GD9mWJeQBgz_UPGXSyOqWPNnH3hARKg4KGB-; dotcom_user=ziboh; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=dark; tz=Asia%2FShanghai; _gh_sess=SEGEdiDJbexQwP608XzUmuv8%2F7U%2FJvAUzYSdTJIYF%2FfabDHZnKXmd%2BQr14LTVRAoEmkTKrQYIzr3oMgdKvwRwx0zae0ha9Q9jxOYQYPROsz%2FOQLxKpmaoAGyb5fXy8jfVrYcuMZBarNS%2BMuPlYVewMzrpjAO9M%2FR4xayrKiclibuEOkmSa%2FF8y8K0uvEGHal%2FzKCQ6ehpC2KDUzTQqD2EtHEMEhrekWNIYwT8LdcjqlBFwzTuAVh9zA7iL31ir5D269IdmpsDYEcSioTXpz0zH7HqWEdt3dpgYxHsJQfnVBBANL8EaEl1ucEE4jUSEX5mjmOdWdm1V5IXoQbRFDKD9RlOjDxj8w6YR9Nko36bo6kf3AMCBDIKZTrlWWEau1Iy1DIU6uQAnwnH5WGxD6zRpodat6vAlE61oSnrOFtfZQs8m1x1eJaiQ2DQdyDxxOUqe1NtUA5XoMNcd4%2FtUBZ15NqRuxMQxzUkiZ%2FQGX6y56tjhfA7P6NDX83rJXmRj5ZX0Efb9%2BV%2BhZT4W47DzhGiorxFtEjyW82JmQEoLJaHww5%2FsUxMG6z%2ByNeG%2B2%2FyfgE3uo90BpBwAwVmhEV%2BnkqDrGUa15smPJLPJP5kJLDEz20O7uyIqzk7z%2BqRJNLkOVPRBiS27aEZt%2BHp8JMBXoolJUMKvzWKbmY0gaHIjnRbj5KD%2FF7Nu5IkyAKk1SsKPOdmCEeIWECd8sjdThYLJ%2BzEwrGUolHQdIBbbZrl6wji%2FdZW%2B4NrwnQ8PhTUDFEFf7Wv05hmSRSp3HHf8VOkUtoM64wR%2Fmrsw1FbYQetNpDvutyU1oLBpSoRB6tTp0nX8TAkCIhyyu4PZl%2FfGzpx0VWC8uOGYkC3tYvuqYjiZo%2Bm9Ni%2FvWC6SUpj%2FaiqCrh1sXhl%2BTFUpTVeZsTQFszRmQpndhFdd1%2FNDpyyfB7Gr5oTkWxmyDWCK8ppNUHYhib1i2UmVHxRnjPQtRDkodnz3Unjk7J84nTG4H%2BGFfFHoxSA0yfKOlvY%2B07WS8C4QeBEEstX5uAZmtVu%2FEUk7R3hEBTdBciEl%2FWDTMHweMDxrOkc3k4dpOCqhTE2VdiKSMXzMUiCrdcbZmSO976Qi1Szysrixj9rl%2BQl0OUIfZqQ82qf3UZ3DslrPbCkeyJmsrbGvksLV1vdxUP8nP6Qm6p1ENSyfgjKZEf12NUTSeKNeHe0961wMG5Gjneu5gl1qxCmm6wdqWPTzidgV19HGJbFrSyJPSnH2aG0HCLI6vw5Ksd056FXSx6zIxgyp3cD7oCrhcoDm8imeIYGbo%3D--jiOKpEtvTnNI8l%2Fc--egQLY7HgndEVvoYNgnPKVw%3D%3D; has_recent_activity=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}

jar = requests.cookies.RequestsCookieJar()
for cookie in cookies.split(";"):
    key,value =cookie.split("=",1)
    jar.set(key,value)
    
    
r  = requests.get("https://github.com",cookies=jar,headers=headers)
# print(r.text)
print(r.cookies.items())

with open("github.html","wb") as f:
    f.write(r.content)
"""

#  session 设置
"""
s = requests.Session()
s.get("https://httpbin.org/cookies/set/name/zibo")
r = s.get("https://httpbin.org/cookies")
print(r.text)
"""
# SSl证书验证

"""
# 会出现警告
response = requests.get("https://ssr2.scrape.center/", verify=False)
print(response.status_code)


# 关闭警告
from requests.packages import urllib3
urllib3.disable_warnings()
response = requests.get("https://ssr2.scrape.center/", verify=False)
print(response.status_code)


# 使用logging捕获异常

import logging

logging.captureWarnings(True)
response = requests.get("https://ssr2.scrape.center/", verify=False)
print(response.status_code)

"""

# indentity auth
"""
from  requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("admin","admin")
response = requests.get("https://ssr3.scrape.center",auth=auth)
print(response.text)
"""

# 使用代理
"""
proxies = {
    "http":"http://192.168.1.2:7893",
    "https":"http://192.168.1.2:7893"
}
response = requests.get("https://www.httpbin.org/get",proxies=proxies)
print(response.text)


# 使用sockes代理(安装requests[socks]包)
proxies = {
    "http":"socks5://192.168.1.2:7893",
    "https":"socks5://192.168.1.2:7893"
}
response = requests.get("https://www.httpbin.org/get",proxies=proxies)
print(response.text)

"""
# prepared Request
# 自定义request请求
"""
from requests import Request ,Session

url = "https://www.httpbin.org/post"
data = {
    "name":"zibo",
    "age":"18"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
proxies = {
    "http":"socks5://proxy.zboh.top:5236",
    "https":"socks5://proxy.zboh.top:5236"
}
s = Session()
req = Request("POST",url=url,headers=headers,data=data)
prepped = s.prepare_request(req)
r = s.send(prepped,proxies=proxies)
print(r.text)
"""
