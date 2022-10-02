import httpx

# httpx的使用和requests基本一致
"""
response = httpx.get("https://www.httpbin.org/get")
print(response.status_code)
print(response.text)
print(response.headers)




headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
}

response = httpx.get("https://httpbin.org/get", headers=headers)
print(response.status_code)
print(response.headers)
print(response.text)
"""

# httpx使用http2.0需要手动开启
"""
response = httpx.get("https://spa16.scrape.center/")
print(response.text)
# httpx.RemoteProtocolError: Server disconnected without sending a response



client = httpx.Client(http2=True)
response = client.get("https://spa16.scrape.center/")
print(response.text)
"""


