import multiprocessing
import os
import requests
from urllib.parse import urljoin
import re
import logging
import json

dir, filename = os.path.split(os.path.realpath(__file__))
logging.basicConfig(level=logging.INFO, filename=f"{dir}\\logging.txt",
                    filemode="w", format="%(asctime)s - %(levelname)s: %(message)s")
BASE_URL = "https://ssr1.scrape.center"
TOTAL_PAGE = 10
RESULTS_DIR = f"{dir}\\results"


def scrape_page(url: str) -> str | None:
    logging.info(f"scraping {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("scraping successfully")
            return response.text
        logging.error(
            f"get invaild status code {response.status_code} while scraping {url}")
        return None
    except requests.RequestException as e:
        logging.error(f"error occurred while scraping {url}")
        return None


def scrape_index(page: int) -> str | None:
    index_url = f"{BASE_URL}/page/{page}"
    return scrape_page(index_url)


def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    detail = re.findall(pattern, html)
    if detail == []:
        return []
    for item in detail:
        detail_url = urljoin(BASE_URL, item)
        logging.info(f"get detail url {detail_url}")
        yield detail_url


def scrape_detail(url):
    return scrape_page(url)


def parse_detail(html):
    img_pattern = re.compile(
        'class="item.*?<img.*?src="(.*?)"\s*class="cover">', re.S)
    name_pattern = re.compile('<h2.*?>(.*?)</h2.*?>', re.S)
    categories_pattern = re.compile(
        '<button.*?class=.*?category.*?<span>(.*?)</span>\s*?</button>', re.S)
    published_at_pattern = re.compile('(\d{4}-\d{1,2}-\d{1,2})\s上映')
    drama_pattern = re.compile(
        '<div.*?class="drama".*?</h3>\s*?<p.*?>(.*?)</p>', re.S)
    score_pattern = re.compile('<p.*?class="score.*?">(.*?)</p>', re.S)
    img_url = re.search(img_pattern, html)
    if img_url:
        img_url = img_url.group(1).strip()
    name = name_pattern.search(html)
    if name:
        name = name.group(1).strip()
    categories = categories_pattern.findall(html)
    published_at = published_at_pattern.search(html)
    if published_at:
        published_at = published_at.group(1).strip()
    drama = drama_pattern.search(html)
    if drama:
        drama = drama.group(1).strip()
    score = score_pattern.search(html)
    if score:
        score = score.group(1).strip()
    return {
        "img_url": img_url,
        "name": name,
        "categories": categories,
        "published_at": published_at,
        "drama": drama,
        "score": score
    }


def main(page: int) -> None:
    index_html = scrape_index(page)
    if index_html:
        detail_urls = parse_index(index_html)
        for detail_url in detail_urls:
            detail_html = scrape_detail(detail_url)
            result = parse_detail(detail_html)
            logging.info(f"get detail data {result}")
            logging.info("saving data to json data")
            save_data(result)
            logging.info("data saved successfully")


def save_data(data):
    if os.name == "nt":
        os.path.exists(RESULTS_DIR) or os.makedirs(RESULTS_DIR)
    elif os.name == "posix":
        os.path.exists(RESULTS_DIR) or os.mkdir(RESULTS_DIR)
    name = data.get("name")
    if name:
        name = re.sub(r'[/:<>"|?\\]', r"-", name)
    data_path = f"{RESULTS_DIR}\\{name}.json"
    json.dump(data, open(data_path, 'w', encoding="utf-8"),
              ensure_ascii=False, indent=2)


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()
