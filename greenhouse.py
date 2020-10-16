from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os # to get the resume file
import time # to sleep
from sys import argv
import pyautogui as page
from form_input_basic_info import JOB_APP

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.touch_actions import TouchActions
from fake_useragent import UserAgent
import random
import undetected_chromedriver as uc
import json
import logging

# To silent webdriver_manager logs and remove them from console
os.environ['WDM_LOG_LEVEL'] = '0'

''' Sign in to gmail and then proceed to the application page. Logging in prior to applying may or may not help avoid captchas.'''
def gmail_login():
    email = 'email'
    password = 'pw'
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(links[0])

    # Enter in login information
    driver.find_element_by_id('identifierId').send_keys(email)
    driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
    time.sleep(2)
    driver.find_element_by_class_name('zHQkBf').send_keys(password)
    driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
    time.sleep(2)

'''These specific options are required to avoid captchas.'''
def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)
options = Options()
userAgent = r"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Mobile Safari/537.36"
options.add_argument(f'user-agent={userAgent}')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-`maximize`d")
options.add_argument("--disable-extensions")

'''Sends input for things that need to be typed.'''
def type_input(action,element,info):
    try:
        action.move_to_element(element)
        action.click(element)
        action.pause(.4)
        for i in info:
            action.send_keys(i)
            action.pause(.2)
        action.perform()
        time.sleep(1)
    except:
        pass

'''Sends input for things that need to be clicked.'''
def click_input(action,element):
    action.move_to_element(element)
    action.click(element)
    action.perform()
    time.sleep(1)

'''Does all the heavy work for applying.'''
def greenhouse(url, counter):
    # Disables annoying logs to the console
    logger = logging.getLogger('undetected_chromedriver').disabled = True

    # Sets up driver (one using regular, another using undetected driver)
    # driver = webdriver.Chrome(executable_path='/Users/chadlei/Downloads/chromedriver')
    driver = uc.Chrome(options=options, executable_path=ChromeDriverManager().install())

    # Changing extra settings
    set_viewport_size(driver, 800, 800)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "driver"}})

    # Getting Recaptcha demo score (optional to see how human your script is)
    # driver.get("https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php")
    # print('Score: ' + str(json.loads(WebDriverWait(driver, 20)
    #     .until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.step3 pre.response")))
    #     .get_attribute("innerHTML"))['score']))

    driver.get(url)

    # basic info
    type_input(ActionChains(driver),driver.find_element_by_id('first_name'),JOB_APP['first_name'])
    type_input(ActionChains(driver),driver.find_element_by_id('last_name'),JOB_APP['last_name'])
    type_input(ActionChains(driver),driver.find_element_by_id('email'),JOB_APP['email'])
    type_input(ActionChains(driver),driver.find_element_by_id('phone'),JOB_APP['phone'])

    # add location
    try:
        click_input(ActionChains(driver),driver.find_element_by_xpath("//a[contains(.,'Locate me')]"))
    except:
        pass

    # Upload Resume
    try:
        driver.find_element_by_xpath('//input[@type="file"]').send_keys(os.getcwd() + JOB_APP['resume'])
        time.sleep(1)
        # resume_element = driver.find_element_by_xpath('//input[@type="file"]')
        # resume_action = ActionChains(driver)
        # resume_action.move_to_element(resume_element)
        # resume_action.send_keys(os.getcwd() + JOB_APP['resume'])
        # resume_action.perform()
        # print('hello')
        # time.sleep(5)
    except NoSuchElementException:
        pass

    # add linkedin
    try:
        type_input(ActionChains(driver),driver.find_element_by_xpath("//label[contains(.,'LinkedIn')]"),JOB_APP['linkedin'])
    except NoSuchElementException:
        pass

    # add full name
    try:
        type_input(ActionChains(driver),driver.find_element_by_xpath("//label[contains(.,'Legal Name')]"),JOB_APP['first_name'] + " " + JOB_APP['last_name'])
    except NoSuchElementException:
        pass

    # add graduation year
    try:
        click_input(ActionChains(driver),driver.find_element_by_xpath("//select/option[text()='2018']"))
    except NoSuchElementException:
        pass

    # add university
    try:
        click_input(ActionChains(driver),driver.find_element_by_xpath("//select/option[contains(.,'Irvine')]"))
    except NoSuchElementException:
        pass

    # add degree
    try:
        click_input(ActionChains(driver),driver.find_element_by_xpath("//select/option[contains(.,'Bachelor')]"))
    except NoSuchElementException:
        pass

    # add major
    try:
        click_input(ActionChains(driver),driver.find_element_by_xpath("//select/option[contains(.,'Computer Science')]"))
    except NoSuchElementException:
        pass

    # add website
    try:
        type_input(ActionChains(driver),driver.find_element_by_xpath("//label[contains(.,'Website')]"),JOB_APP['website'])
    except NoSuchElementException:
        pass

    # add work authorization
    try:
        el = driver.find_element_by_xpath("//label[contains(.,'authoriz')]/select")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'Yes':
                option.click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # add sponsorship
    try:
        el = driver.find_element_by_xpath("//label[contains(.,'require sponsorship')]/select")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'No':
                option.click()
        time.sleep(1)
    except NoSuchElementException:
        pass
    try:
        el = driver.find_element_by_xpath("//label[contains(.,'do not need any form of sponsorship')]/select")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'Yes':
                option.click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # add work experience time line
    try:
        el = driver.find_element_by_xpath("//label[contains(.,'working experience')]/select")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'No':
                option.click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # add relocation
    try:
        el = driver.find_element_by_xpath("//label[contains(.,'comfortable') or contains(., 'relocat')]/select")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'Yes':
                option.click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # add salary expectations
    try:
        type_input(ActionChains(driver),driver.find_element_by_xpath("//label[contains(.,'salary expectations')]"),'70,000')
    except NoSuchElementException:
        pass

    # add most recent employer
    try:
        type_input(ActionChains(driver),driver.find_element_by_xpath("//label[contains(.,'Current')]"),JOB_APP['most_recent_employer'])
    except NoSuchElementException:
        pass

    # add reason why I want to work at the company
    try:
        type_input(ActionChains(driver),driver.find_element_by_xpath("//label[contains(.,'want to work')]"),JOB_APP['reason_of_interest'])
    except NoSuchElementException:
        pass

    # add where I heard about job from
    try:
        type_input(ActionChains(driver),driver.find_element_by_xpath("//label[contains(.,'hear about this job')]"),"Linkedin")
    except NoSuchElementException:
        pass

    # add years of experience
    try:
        el = driver.find_element_by_xpath("//label[contains(.,'years of')]/select")
        for option in el.find_elements_by_tag_name('option'):
            if 'or less' in option.text:
                option.click()
        time.sleep(1)
    except NoSuchElementException:
        pass

    # Submit the app
    try:
        click_input(ActionChains(driver),driver.find_element_by_id("submit_app"))
    except NoSuchElementException:
        pass

    # Checks for successful application
    completed = False
    while (not completed):
        try:
            myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'application_confirmation')))
            print(str(counter) + ' Success!')
            completed = True
            return True
        except TimeoutException:
            # It'll keep waiting for you to manually complete the application if it doesn't auto complete
            print("URL - " + url + " requires attention... check it")
            time.sleep(5)









'''You can manually test the function here.'''
if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    try:
        greenhouse(url1)
        # gmail_login()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        driver.close()
    except NoSuchElementException:
        print('NoSuchElementException')
        driver.close()
    except NameError as e:
        print(e)
        driver.close()
    driver.close()
