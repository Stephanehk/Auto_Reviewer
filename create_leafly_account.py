import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import json
from random import randint
import time

def random_with_N_digits(n):
    #https://stackoverflow.com/questions/2673385/how-to-generate-random-number-with-the-specific-length-in-python
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def generate_account (data, user):
    #format user data
    name = user["name"].split(" ")
    firstname, lastname, username, password = name[0], name[1], user["username"], user["password"]

    delay = 20
    url = "https://www.leafly.com/"

    #suck my dick admin
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)

    #load website
    driver = webdriver.Chrome("/Users/2020shatgiskessell/Desktop/auto_reviewer/chromedriver",chrome_options=options)
    driver.get(url)
    time.sleep(5)

    #press yes (older than 21)
    driver.find_element_by_css_selector(".button.ml-md").click()
    #press sidebar
    driver.find_element_by_css_selector(".block.relative.mr-md.p-xs").click()
    time.sleep(2)
    #press login/signup
    driver.find_element_by_class_name("nav__item").click()
    time.sleep(2)
    #press join us
    element = driver.find_element_by_class_name("ml-sm").click()
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(2)

    driver.find_element_by_id("email").send_keys(username + "@yandex.com")
    #enter username
    driver.find_element_by_id("username").send_keys(username)
    #enter password
    driver.find_element_by_id("password").send_keys(password)


    #hit agree to terms and services
    element = driver.find_element_by_css_selector(".checkbox__checkbox-input")
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(1)

    #join us
    driver.find_element_by_xpath('//*[@id="sso-content"]/div/form/button').click()

    #modify users JSON
    for account in data["accounts"]:
        if account["password"] == password:
            account["yelp_reviewed"] = "true"
    with open('generated_accounts.txt', 'w') as outfile:
        json.dump(data, outfile)


with open('generated_accounts.txt') as json_file:
    data = json.load(json_file)

accounts = data["accounts"]
user = accounts[0]
generate_account (data,user)
