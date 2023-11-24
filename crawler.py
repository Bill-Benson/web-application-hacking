import requests

target_url = "10.0.2.27/mutillidae/"


def request(url):
    try:
        get_response = requests.get("http://" + url)
        return get_response
    except requests.exceptions.ConnectionError:
        pass


with open("files-and-dirs-wordlist.txt", "r") as wordlist:
    for line in wordlist:
        word = line.strip()
        directory = target_url + word
        response = request(directory)
        if response:
            print("[+] Discovered directory --> " + directory)
