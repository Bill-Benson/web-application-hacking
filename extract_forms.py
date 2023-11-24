from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup  # Import BeautifulSoup from the bs4 module

target_url = "http://10.0.2.27/mutillidae/index.php?page=user-info.php"


def make_request(url):
    try:
        get_response = requests.get(url)
        return get_response
    except requests.exceptions.ConnectionError:
        pass


response = make_request(target_url)

# Check if the response is not None before using BeautifulSoup
if response:
    parsed_html = BeautifulSoup(response.content.decode("utf-8"))
    forms_list = parsed_html.findAll("form")

    # Now you can work with the forms_list
    for form in forms_list:
        action = form.get("action")
        method = form.get("method")
        post_url = urljoin(target_url, action)

        post_data_dict = {}
        input_list = form.findAll("input")
        for input_ in input_list:
            input_name = input_.get("name")
            input_value = input_.get("value")
            input_type = input_.get("type")
            if input_type == "text":
                input_value = "test"

            post_data_dict[input_name] = input_value
        result = requests.post(post_url, data=post_data_dict)
        print(result.content.decode("utf-8"))
else:
    print("Failed to retrieve the page.")
