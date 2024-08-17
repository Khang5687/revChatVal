import pathlib
from utils import save_cookies, load_cookies, stringify_cookies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def next_btn(driver, wait_time=10) -> None:
    """Press the 'Next' button on the Microsoft login page. aka. the Blue one

    Args:
        driver (_type_): Chrome webdriver
        wait_time (_int_): Time to wait for the element to be clickable, default is 10 seconds
    """

    stay_logged_in_btn_xpath = "//input[@id='idSIButton9']"
    stay_logged_in_btn = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, stay_logged_in_btn_xpath))
    )
    stay_logged_in_btn.click()


def login(email, password) -> str:
    """Proceeds login to RMIT Microsoft account and retrieves cookies from val.rmit.edu.au

    Args:
        email (str): email
        password (str): password

    Returns:
        str: cookie value as string
    """
    # Initialize WebDriver, allocating a user-data-dir to store cookies
    # user-data-dir: .\selenium
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={pathlib.Path().absolute()}\\selenium")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to target URL
    driver.get("https://val.rmit.edu.au/")

    # Wait for redirection to Microsoft Authentication login page
    try:
        element = WebDriverWait(driver, 1000).until(
            EC.any_of(
                EC.presence_of_element_located((By.ID, "i0116")),
                EC.presence_of_element_located((By.ID, "i0118")),
            )
        )
    except:
        print("Already logged in")
        # Retrieve all cookies
        cookies = driver.get_cookies()

        driver.quit()

        # Return or print the cookie value
        if cookies:
            return stringify_cookies(cookies)
        else:
            return None

    if element.get_attribute("id") == "i0116":
        element.send_keys(email)
        next_btn(driver)

        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "i0118"))
        )
        password_input.send_keys(password)
    else:
        element.send_keys(password)

    next_btn(driver)

    # After entered the password, if 2FA is enabled, click on "Remember for 30 days"
    remember_checkbox = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "idLbl_SAOTCAS_TD_Cb"))
    )
    remember_checkbox.click()

    twofa_code = (
        WebDriverWait(driver, 10)
        .until(EC.visibility_of_element_located((By.ID, "idRichContext_DisplaySign")))
        .text
    )

    print(f"2FA detected! verify on mobile authenticator: code is {twofa_code}")

    # If is prompted for "Stay signed in?" click on "Yes"
    next_btn(driver, wait_time=200)  # <- Wait time 30s is waiting for 2FA confirmation

    # Wait for redirection back to val.rmit.edu.au
    WebDriverWait(driver, 10).until(EC.url_to_be("https://val.rmit.edu.au/"))

    # Retrieve all cookies
    cookies = driver.get_cookies()

    cookies_dict = {}

    for cookie in cookies:
        cookies_dict[cookie["name"]] = cookie["value"]

    driver.quit()

    # Return or print the cookie value
    if cookies:
        save_cookies(cookies_dict)
        return stringify_cookies(cookies_dict)
    else:
        return None
