import os
import json


def save_cookies(cookie_value):
    print("Fuckye\n\n")
    # Open the cookies.json file in write mode
    with open("cookies.json", "w") as file:
        json.dump(cookie_value, file)


def load_cookies():
    # Check if the cookies.json file exists
    if not os.path.exists("cookies.json"):
        return None

    # Open the cookies.json file in read mode
    with open("cookies.json", "r") as file:
        # Load the cookie data
        try:
            cookie_data = json.load(file)
        except:
            cookie_data = None

    return cookie_data
