import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import string
import random
import json


def randomString(stringLength):
    #https://pynative.com/python-generate-random-string/
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



def generate_account (username, password):
    delay = 20
    #url = 'https://protonmail.com/'
    url = "https://mail.protonmail.com/create/new?language=en"

    #fuck u admin
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)

    #load website
    driver = webdriver.Chrome("/Users/2020shatgiskessell/Desktop/auto_reviewer/chromedriver",chrome_options=options)
    driver.get(url)

    # #press signup button
    # driver.find_element_by_xpath("//*[contains(text(), 'SIGN UP')]").click()
    # time.sleep(2)
    #
    # #click on free plan
    # driver.find_element_by_class_name("panel-heading").click()
    # time.sleep(2)
    #
    # #press select free plan
    # driver.find_element_by_xpath("//*[contains(text(), 'SELECT FREE PLAN')]").click()
    time.sleep(5)

    #create username and password
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    driver.find_element_by_id("username").send_keys(username)
    driver.switch_to.default_content()
    time.sleep(5)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(2)
    driver.find_element_by_id("passwordc").send_keys(password)
    time.sleep(2)

    #hit submit and confirm
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[1])
    driver.find_element_by_xpath("//*[@class='btn btn-submit']").click()
    driver.switch_to.default_content()
    time.sleep(5)
    driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]").click()
    time.sleep(2)

    #--------------------get around captcha--------------------
    #get recovery email
    with open('generated_accounts.txt') as json_file:
        data = json.load(json_file)
        recovery_email_raw = data["gmx_accounts"][-1]
        recovery_email = {"username":recovery_email_raw["username"], "password":recovery_email_raw["password"]}
    data["accounts"].append({"username":username,"password":password,"recovery_email":recovery_email})
    with open('generated_accounts.txt', 'w') as outfile:
        json.dump(data, outfile)

    #select verify email
    #id-signup-radio-email
    driver.find_element_by_id("id-signup-radio-email").click()
    time.sleep(2)
    #enter email
    driver.find_element_by_id("emailVerification").send_keys(recovery_email["username"] + "@protonmail.com")
    #wolandhasarrived@gmail.com
    #driver.find_element_by_id("emailVerification").send_keys("wolandhasarrived@gmail.com")
    time.sleep(2)
    #press send
    driver.find_element_by_xpath("//*[contains(text(), 'Send')]").click()
    time.sleep(5)

generate_account (randomString(10), randomString(10))
