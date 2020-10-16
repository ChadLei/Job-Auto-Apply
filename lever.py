from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os # to get the resume file
import time # to sleep
from sys import argv


# sample applications
URL_g2 = 'https://boards.greenhouse.io/pricespider/jobs/4641394002?s=LinkedIn&source=LinkedIn#app'
URL_l2 = 'https://jobs.lever.co/mheducation/fe0edeff-a8da-446a-b263-14e66c648e68/apply?lever-source=LinkedIn%20Wrap%20Board'


# there's probably a prettier way to do all of this
URLS = [URL_l2] # to test all the URLS

# Fill in this dictionary with your personal details!
JOB_APP = {
    "first_name": "Chad",
    "last_name": "Lei",
    "email": "cblei@uci.edu",
    "phone": "415-722-8190",
    "org": "Perficient",
    "resume": "resume.pdf",
    "resume_textfile": "",
    "linkedin": "https://www.linkedin.com/in/chad-lei-5976918b/",
    "website": "https://github.com/ChadLei/",
    "github": "https://github.com/ChadLei/",
    "twitter": "",
    "location": "Irvine, California, United States",
    "grad_month": '06',
    "grad_year": '2018',
    "university": "University of California, Irvine" # not tru
}

# Handle a Lever form
def lever(driver):
    # navigate to the application page
    driver.find_element_by_class_name('template-btn-submit').click()

    # basic info
    first_name = JOB_APP['first_name']
    last_name = JOB_APP['last_name']
    full_name = first_name + ' ' + last_name  # f string didn't work here, but that's the ideal thing to do
    driver.find_element_by_name('name').send_keys(full_name)
    driver.find_element_by_name('email').send_keys(JOB_APP['email'])
    driver.find_element_by_name('phone').send_keys(JOB_APP['phone'])
    driver.find_element_by_name('org').send_keys(JOB_APP['org'])
    time.sleep(1)

    # socials
    driver.find_element_by_name('urls[LinkedIn]').send_keys(JOB_APP['linkedin'])
    # driver.find_element_by_name('urls[Twitter]').send_keys(JOB_APP['twitter'])
    try: # try both versions
        driver.find_element_by_name('urls[Github]').send_keys(JOB_APP['github'])
    except NoSuchElementException:
        try:
            driver.find_element_by_name('urls[GitHub]').send_keys(JOB_APP['github'])
        except NoSuchElementException:
            pass
    try:
        driver.find_element_by_name('urls[Portfolio]').send_keys(JOB_APP['website'])
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add university
    try:
        driver.find_element_by_class_name('application-university').click()
        search = driver.find_element_by_xpath("//*[@type='search']")
        search.send_keys(JOB_APP['university']) # find university in dropdown
        search.send_keys(Keys.RETURN)
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add how you found out about the company
    # try:
    #     driver.find_element_by_class_name('application-dropdown').click()
    #     search = driver.find_element_by_xpath("//select/option[text()='Glassdoor']").click()
    # except NoSuchElementException:
    #     pass

    # add work authorization
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'authorized to work')]/following::input[1]").click()
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add sponsorship
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'sponsor')]/following::input[2]").click() # Finds radio button
    except:
        try:
            driver.find_element_by_xpath("//div/div[contains(.,'sponsor')]/following::option[2]").click() # Finds select drop down
        except NoSuchElementException:
            pass
    time.sleep(1)

    # add previously worked
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'previously been employed')]/following::option[2]").click() # Finds select drop down
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add working with company
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'currently a')]/following::option[2]").click() # Finds select drop down
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add background check
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'background screening')]/following::option[2]").click() # Finds select drop down
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add salary expectations
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'Salary')]/following::input[1]").send_keys('80,000')
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add Street address
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'Address')]/following::input[1]").send_keys('14941 Mayten Ave')
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add City
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'City')]/following::input[1]").send_keys('Irvine')
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add State
    try:
        # driver.find_element_by_xpath("//div/div[starts-with(.,'State')]/following::input[1]").click()
        driver.find_element_by_xpath("//div/div[starts-with(.,'State')]/following::input[1]").send_keys('California')
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add Zipcode
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'Zipcode')]/following::input[1]").send_keys('92606')
    except NoSuchElementException:
        pass
    time.sleep(1)

    # add Country of Residence
    try:
        driver.find_element_by_xpath("//div/div[contains(.,'Country')]/following::input[1]").send_keys('United States')
    except NoSuchElementException:
        pass

    # submit resume last so it doesn't auto-fill the rest of the form
    # since Lever has a clickable file-upload, it's easier to pass it into the webpage
    driver.find_element_by_name('resume').send_keys(os.getcwd()+"/resume.pdf")
    time.sleep(500)
    driver.find_element_by_class_name('template-btn-submit').click()
    time.sleep(25)

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='/Users/ChazeiChazy/downloads/Scripts/chromedriver')

    try:
        url = argv[1]
        driver.get(url)
        lever(driver)
    except KeyboardInterrupt:
        driver.close()
    driver.close()
