import json
import re
import time
import requests
from urllib.parse import urljoin
import logging
import os
from lxml import etree


DIR = os.path.dirname(__file__)
BASE_URL = "https://www.sehuatang.org"
PROXIES = {
    "http": "http://192.168.1.2:7893",
    "https": "http://192.168.1.2:7893"
}
TOTAL_PAGE = 100
TMP_HTML = os.path.join(DIR, "tmp.html")
SAVE_DIR = os.path.join(DIR, "sehuatang")
now_time = time.strftime("%Y-%m-%d %H-%M", time.localtime())
LOG_FILENAME = f'{now_time}.log'
LOG_DIR = os.path.join(DIR, "log")
DELAY_TIME = 2
FILE_NOT_EXISTS_COUNT = 10
change_file_count = 0
os.path.exists(LOG_DIR) or os.mkdir(LOG_DIR)
logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(LOG_DIR, LOG_FILENAME),
                    filemode="a",
                    format="%(asctime)s - %(levelname)s: %(message)s")

def scrape_page(url: str) -> str | None:
    try:
        response = requests.get(url=url, proxies=PROXIES)
        if response.status_code == 200:
            logging.info(f"page scraped successfully while is {url}")
            return response.text
        else:
            logging.error(
                f"get invaild status code {response.status_code} while is {url}")
    except requests.RequestException:
        logging.error("get request error")

def scrape_index(page: int) -> str | None:
    index_url = BASE_URL + "/forum-103-" + str(page) + ".html"
    page = scrape_page(index_url)
    if page is None:
        page = repeat_request_page(index_url)
    return page

def get_content_url_title(html):
    html_etree = etree.HTML(html)
    result = html_etree.xpath(
        '//form/table/tbody[contains(@id,"normalthread")]/tr/th/a[2]')
    if result is None:
        ERROR_PAGE = os.path.join(DIR, "error_page")
        os.path.exists(ERROR_PAGE) or os.mkdir(ERROR_PAGE)
        logging.error(
            "This page get content url fail , the index page save in .\\error_page\\get_content_url_title.html")
        filepath = os.path.join(ERROR_PAGE, "get_content_url_title.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        os._exit(0)

    return map(lambda x: (urljoin(BASE_URL, x.attrib["href"]), x.text), result)

def parse_content(html):
    data = {}
    html_etree = etree.HTML(html)
    xpath_result = html_etree.xpath('//*[contains(@id,"postmessage")]')
    if not xpath_result:
        ERROR_PAGE = os.path.join(DIR, "error_page")
        os.path.exists(ERROR_PAGE) or os.mkdir(ERROR_PAGE)
        logging.error(
            "This page parse_content fail , the content page save in .\\error_page\\content.html")
        filepath = os.path.join(ERROR_PAGE, "content.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return None
    content = xpath_result[0]

    # 获取标题文本
    title_text = html_etree.xpath('//*[@id="thread_subject"]/text()')
    original_title = title_text[0]
    match_result = re.search("([A-Za-z-_0-9]{5,})(.*?)$", original_title)
    if match_result is None:
        ERROR_PAGE = os.path.join(DIR, "error_page")
        os.path.exists(ERROR_PAGE) or os.mkdir(ERROR_PAGE)
        logging.error(
            "This page parse_content fail , the content page save in .\\error_page\\content.html")
        filepath = os.path.join(ERROR_PAGE, "content.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return None
    title = match_result.group(1) + match_result.group(2)
    title_number = match_result.group(1).strip()
    title_name = match_result.group(2).strip()
    data["title"] = title
    data["title_number"] = title_number
    data["title_name"] = title_name

    ismosaic_text = html_etree.xpath(
        '//*[@id="thread_subject"]/parent::*/a/text()')
    ismosaic = ismosaic_text[0].strip('[]')
    data["ismosaic"] = ismosaic
    # 获取磁力
    try:
        mangent_list = []
        magnent_nodes = content.xpath('//div[@class="blockcode"]//li')
        for magnent_node in magnent_nodes:
            mangent = magnent_node.text
            if mangent is None:
                continue
            match_result =  re.search("(magnet:\?xt=urn:btih:[0-9a-zA-Z]{32})",mangent)
            if match_result:
                mangent_list.append(match_result.group(1)) 
    except Exception as e:
        logging.info(e)
        return None
    
    data["mangent"] = mangent_list
    # 正文里的中文标题
    chinese_name = content.text.replace("【影片名称】：", "").strip()
    if chinese_name == "":
        chinese_name = title_name
    data["chinese_name"] = chinese_name

    return data

def save_data(data):
    filename = data.get("title")
    filename = re.sub(r'[/:<>"|?\\]', r"-", filename)
    file_path = os.path.join(SAVE_DIR, f"{filename}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def repeat_request_page(url, count=5):
    for i in range(1, count+1):
        time.sleep(DELAY_TIME)
        logging.warning(f"The {i+1}th request to {url}")
        page = scrape_page(url)
        if page is not None:
            break
    return page

def get_max_page():
    page = scrape_index(1)
    with open(TMP_HTML, "w", encoding="utf-8") as f:
        f.write(page)
    html = etree.HTML(page)
    page_num = html.xpath('//a[contains(@href,"forum") and @class="last"]')
    if page_num[0].text == page_num[1].text:
        return eval(page_num[0].text.strip(". "))

def delect_error_json():
    deleted_file_count = 0
    os.chdir(SAVE_DIR)
    filedir = os.listdir()
    for i in filedir:
        match_result = re.match("([a-zA-Z0-9-_])", i)
        if match_result is None:
            deleted_file_count += 1
            os.remove(i)
    logging.info(f"{deleted_file_count} files have deleted")

def main():
    # 连续错误次数
    continuous_error = 0
    # 总共错误次数
    total_error = 0

    os.path.exists(SAVE_DIR) or os.mkdir(SAVE_DIR)
    max_pages = get_max_page()
    total_pages = max_pages if max_pages else TOTAL_PAGE
    for i in range(1, total_pages + 1):
        html = scrape_index(i)
        content_count = 0

        if html is None:
            logging.error(f"page {i} is request fail")
            os._exit(0)
        urls = get_content_url_title(html)

        for conten_url, content_title in urls:
            content_count += 1

            re_result = re.search("([A-Za-z-_0-9][A-Za-z-_0-9]{5,})(.*?)$", content_title)
            content_title = re_result.group(1) + re_result.group(2)
            content_title = re.sub(r'[/:<>"|?\\]', r"-", content_title)

            filepath = os.path.join(SAVE_DIR, f"{content_title}.json")
            if os.path.exists(filepath):
                logging.info(f'{content_title} already exist\n\n\n')
                continue
            content_html = scrape_page(conten_url)

            if content_html is None:
                content_html = repeat_request_page(conten_url)

                if content_html is None:
                    continuous_error += 1
                    total_error += 1
                    logging.error(
                        f"{conten_url} scrape fail ,{total_error} errors in total")
                    print(f"{conten_url} scrape fail")
                    print(f"total error is {total_error}")
                    if continuous_error >= 5:
                        logging.error(f"more five continuous error")
                        os._exit(0)
                    continue

            continuous_error = 0
            data = parse_content(content_html)
            if data is None:
                continue
            data["url"] = conten_url
            logging.info(data)
            logging.info("saving data to json file")
            save_data(data)
            logging.info("saved data successfully\n\n\n")
            time.sleep(DELAY_TIME)

        logging.info(
            f"Page {i} scraped Complet,This page has {content_count} contents\n\n\n")
        print(f"Page {i} scraped Complet,This page has {content_count} contents")
    
def del_tag_json(tag="ismosaic"):
    os.chdir(SAVE_DIR)
    for filename in os.listdir():
        with open(filename, "r+", encoding="utf-8") as f:
            data = json.load(f)
            if data.get(tag) is not None:
                del data[tag]
                f.seek(0)
                f.truncate()
                json.dump(data, f, ensure_ascii=False, indent=2)
                global change_file_count
                change_file_count += 1
                logging.info(f"{change_file_count} files have changed")

def add_tag_to_json(filepath, tag, tag_data):
    try:
        with open(filepath, "r+", encoding="utf-8") as f:
            data = json.load(f)
            if data.get(tag) is None:
                global change_file_count
                change_file_count += 1
                data[tag] = tag_data
                f.seek(0)
                f.truncate()
                json.dump(data, f, ensure_ascii=False, indent=2)
                logging.info(f"{change_file_count} files have changed")
            return True
    except Exception as e:
        print(e)
        logging.error(f"{filepath} open fail")
        return False

def check_tag(tag = "ismosaic"):
    os.chdir(SAVE_DIR)
    for filename in os.listdir():
        with open(filename, "r+", encoding="utf-8") as f:
            data = json.load(f)
            if data.get(tag) is None:
                print(filename)

def parse_ismosaic(html):
    html_etree = etree.HTML(html)
    result = html_etree.xpath(
        '//form/table/tbody[contains(@id,"normalthread")]/tr/th')
    return map(lambda x: (x.getchildren()[1].getchildren()[0].text, x.getchildren()[2].text), result)
    
def add_tag():
    continuous_error = 0
    max_pages = get_max_page()
    total_pages = max_pages if max_pages else TOTAL_PAGE
    for i in range(1, total_pages + 1):
        html = scrape_index(i)

        if html is None:
            logging.error(f"page {i} is request fail")
            os._exit(0)
        for ismosaic, content_title in parse_ismosaic(html):
            re_result = re.search("([A-Za-z-_0-9]+)(.*?)$", content_title)
            content_title = re_result.group(1) + re_result.group(2)
            content_title = re.sub(r'[/:<>"|?\\]', r"-", content_title)
            filepath = os.path.join(SAVE_DIR, f"{content_title}.json")
            if not add_tag_to_json(filepath, "ismosaic", ismosaic):
                continuous_error += 1
                if continuous_error > 9:
                    os._exit(0)



if __name__ == "__main__":
    # main()
    with open(os.path.join(DIR,"123.html"),"r",encoding="utf-8") as f:
        html = f.read()
        print(parse_content(html))

                    
