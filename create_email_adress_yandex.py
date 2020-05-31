import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import string
import random
import json
import urllib.request
import cv2
import pytesseract
import numpy as np
import captcha_solver
from captcha_solver import CaptchaSolver
import names

def randomString(stringLength):
    #https://pynative.com/python-generate-random-string/
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def break_captcha(driver):
    #get captcha image
    try:
        img = driver.find_element_by_class_name("captcha__image")
        src = img.get_attribute('src')
        urllib.request.urlretrieve(src, "captcha.png")

        solver = CaptchaSolver('rucaptcha', api_key='bef7004b9dcbbcba502cd826f2bafa49')
        raw_data = open('captcha.png', 'rb').read()
        captcha_text = solver.solve_captcha(raw_data)
    except captcha_solver.error.CaptchaServiceError:
        driver.find_element_by_class_name("captcha__image").click()
        break_captcha(driver)
    return captcha_text

def generate_account (firstname, lastname):
    delay = 20
    #url = 'https://protonmail.com/'
    url = "https://passport.yandex.com/registration/mail?from=mail&require_hint=1&origin=hostroot_homer_reg_com&retpath=https%3A%2F%2Fmail.yandex.com%2F&backpath=https%3A%2F%2Fmail.yandex.com%3Fnoretpath%3D1"

    #suck my dick admin
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)

    #load website
    driver = webdriver.Chrome("/Users/2020shatgiskessell/Desktop/auto_reviewer/chromedriver",chrome_options=options)
    driver.get(url)
    time.sleep(5)

    #decline cookies
    driver.find_element_by_xpath("//*[contains(text(), 'Decline')]").click()
    #enter first name
    driver.find_element_by_name("firstname").send_keys(firstname)
    #enter last name
    driver.find_element_by_name("lastname").send_keys(lastname)
    #enter username
    username = firstname+randomString(8)
    driver.find_element_by_name("login").send_keys(username)
    #enter/confirm password

    password = randomString(10)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("password_confirm").send_keys(password)
    #time.sleep(5)
    #press I dont have a phone number
    #driver.find_element_by_class_name("fetching-block").click()
    #driver.find_element_by_xpath("//*[contains(text(), ''I don't have a mobile phone'')]").click()
    try:
        element = driver.find_element_by_css_selector(".toggle-link.link_has-no-phone")
        ActionChains(driver).move_to_element(element).click().perform()
        time.sleep(5)
        #enter security question
        try:
            WebDriverWait(driver, 20).until(driver.find_element_by_name("hint_answer").send_keys(randomString(5)))
            time.sleep(5)
        except TypeError:
            pass
    except Exception as e:
        print ("failed, trying again...")
        print (e)
        generate_account (randomString(12), randomString(10))

    #break captcha
    captcha_text = break_captcha(driver)
    driver.find_element_by_name("captcha").send_keys(captcha_text)

    #press submit
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/button').click()
    time.sleep(2)
    #press accept
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button').click()
    time.sleep(2)



    with open('generated_accounts.txt') as json_file:
        data = json.load(json_file)

    #delete and uncomment above after first email created
    # data = {}
    # data["accounts"] = []

    data["accounts"].append({"username":username,"password":password,"name":firstname + " " + lastname, "yelp_reviewed":"false"})
    with open('generated_accounts.txt', 'w') as outfile:
        json.dump(data, outfile)

def generate_multiple_accounts(n):
    for i in range (n):
        generate_account (names.get_first_name(), names.get_last_name())
