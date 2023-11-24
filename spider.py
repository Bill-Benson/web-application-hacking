import re
import requests
from urllib.parse import urljoin

target_url = "http://10.0.2.27/mutillidae/"


def extract_links_from(url):
    response = requests.get(url)
    html_code = response.content
    return re.findall(rb'href=["\'](.*?)["\']', html_code)


target_links = []


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        full_link = urljoin(url, link.decode("utf-8"))
        if "#" in full_link:
            full_link = full_link.split("#")[0]
        if target_url in full_link and full_link not in target_links:
            target_links.append(full_link)
            print(full_link)
            crawl(full_link)


crawl(target_url)
