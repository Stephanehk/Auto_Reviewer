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
    url = "https://www.yelp.com/signup?return_url=https://www.yelp.com/seeyousoon"

    #suck my dick admin
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)

    #load website
    driver = webdriver.Chrome("/Users/2020shatgiskessell/Desktop/auto_reviewer/chromedriver",chrome_options=options)
    driver.get(url)
    time.sleep(5)


    #enter first name
    driver.find_element_by_id("first_name").send_keys(firstname)
    #enter last name
    driver.find_element_by_id("last_name").send_keys(lastname)
    #enter email
    driver.find_element_by_id("email").send_keys(username + "@yandex.com")
    #enter password
    driver.find_element_by_id("password").send_keys(password)
    #enter zipcode
    zip = random_with_N_digits(5)
    driver.find_element_by_id("zip").send_keys(zip)

    #hit submit
    driver.find_element_by_xpath('//*[@id="signup-button"]').click()
    time.sleep(5)
    try:
        #are you a human test
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]').click()
        driver.switch_to.default_content()

        #hit submit
        driver.find_element_by_xpath('//*[@id="signup-button"]').click()
        time.sleep(2)
    except selenium.common.exceptions.WebDriverException as e:
        print (e)
        print ("no robot check")
    #hit skip
    element = driver.find_element_by_css_selector(".skip")
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(5)

    #modify users JSON
    for account in data["accounts"]:
        if account["password"] == password:
            account["yelp_reviewed"] = "true"
    with open('generated_accounts.txt', 'w') as outfile:
        json.dump(data, outfile)


with open('generated_accounts.txt') as json_file:
    data = json.load(json_file)

accounts = data["accounts"]
user = accounts[1]
generate_account (data,user)
