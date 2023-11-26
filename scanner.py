"""
Module to be called by the vulnerability scanner to chech for XSS vulnerabilities
"""

from urllib.parse import urljoin
from bs4 import BeautifulSoup  # Import BeautifulSoup from the bs4 module
import requests
import re


class Scanner:
    def __init__(self, url, ignore_links):
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links
        self.session = requests.Session()

    def extract_links_from(self, url):
        response = self.session.get(url)
        html_code = response.content
        return re.findall(rb'href=["\'](.*?)["\']', html_code)

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            full_link = urljoin(url, link.decode("utf-8"))
            if "#" in full_link:
                full_link = full_link.split("#")[0]
            if (self.target_url in full_link and full_link not in self.target_links
                    and full_link not in self.links_to_ignore):
                self.target_links.append(full_link)
                print(full_link)
                self.crawl(full_link)

    def extract_form(self, url):
        response = self.session.get(url)
        if response:
            parsed_html = BeautifulSoup(response.content.decode("utf-8", errors="ignore"), features="lxml")
            return parsed_html.findAll("form")
        else:
            print("Failed to retrieve the page.")

    def submit_form(self, form, value, url):
        action = form.get("action")
        method = form.get("method")
        post_url = urljoin(url, action)

        post_data_dict = {}
        input_list = form.findAll("input")
        for input_ in input_list:
            input_name = input_.get("name")
            input_value = input_.get("value")
            input_type = input_.get("type")
            if input_type == "text":
                input_value = value

            post_data_dict[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data_dict)
        return self.session.get(post_url, params=post_data_dict)

    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>('test')</scriPt>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.content.decode("utf-8", errors="ignore")

    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>('test')</scriPt>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.content.decode("utf-8", errors="ignore")

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_form(link)
            for form in forms:
                print("[+] Testing forms in " + link)
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss:
                    print("\n\n[+++] XSS DISCOVERED in {} in form {}".format(link, form), "\n")

            if "=" in link:
                print("[+] Testing " + link)
                is_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                    print("\n\n[+++] XSS DISCOVERED in {}".format(link), "\n")
                
