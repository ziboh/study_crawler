from lxml import etree
import os
BASE_URL = "https://www.sehuatang.org"
DIR,FILENAME = os.path.split(os.path.realpath(__file__))


html = etree.parse(f"{DIR}/tmp.html",etree.HTMLParser())
a = html.xpath('//form/table/tbody[contains(@id,"normalthread")]/tr/th/a[2]/@href')
b = list(map(lambda x : BASE_URL + "/" + x,a))
print(b,len(b))
