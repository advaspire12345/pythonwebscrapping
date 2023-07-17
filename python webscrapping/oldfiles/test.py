from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys as k
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import os
import requests
from selenium.webdriver.common.action_chains import ActionChains
import random
import urllib
import re
from datetime import datetime
import json
from selenium.webdriver.common.keys import Keys
import test221110

PATH = r"C:\Users\khsra\Desktop\python webscrapping\chromedriver\chromedriver.exe"
websitePath = "https://www.facebook.com/"
USERNAME = "erikaariffin90@gmail.com"
PASSWORD = "Erikaariffin_90"
print(PATH)
print(USERNAME)
print(PASSWORD)

driver = webdriver.Chrome(PATH)

driver.get("https://www.facebook.com/")

email = driver.find_element(By.ID, "email")
email.send_keys(USERNAME)
password = driver.find_element(By.ID, "pass")
password.send_keys(PASSWORD)
time.sleep(1)
password.send_keys(Keys.RETURN)

print(driver.current_url)

action = ActionChains(driver)

RANDOM_CAT_ID = [{"category_ID": "C1639059613", "title": "Property"},
                    {"category_ID": "C1644386246", "title": "Recruitment"},
                    {"category_ID": "C1649236426", "title": "Digital Marketing"},
                    {"category_ID": "C1652755672", "title": "Healthcare"},
                    {"category_ID": "C1656578687", "title": "Beauty"}]

print(RANDOM_CAT_ID)

NEWSFEED_SCRAPER = True
POSTS = []
NO_MORE_POSTS = False

print("running line 56")

only_int = []
share_count = 0
comments_count = 0

sponsor_class = "x15bjb6t x1qlqyl8 xjb2p0i xt0psk2 x9f619"

SCROLL_PAUSE_TIME = 5
# e = driver.find_element(By.TAG_NAME, 'body')
# e.click()
# Get scroll height
lh = driver.execute_script("return document.body.scrollHeight")
if NEWSFEED_SCRAPER:
    # rimuovi la barra bianca di facebook che da problemi e a volte viene cliccato in automatico
    topbar = driver.find_elements(By.XPATH, '//*[@role="banner"]')
    if len(topbar):
        driver.execute_script('arguments[0].remove();', topbar[0])
    while not NO_MORE_POSTS:
        # Scroll down to bottom
        action.scroll_by_amount(0, 50).perform()
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        print("I'm scrolling down 50 lines")
        time.sleep(SCROLL_PAUSE_TIME)

        only_int = []
        share_count = 0
        comments_count = 0

        for i in range(20):
            action.scroll_by_amount(0, 200).perform()
            p = driver.find_elements(By.CSS_SELECTOR, "a[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']:not(.seen)")

            if not len(p):
                NO_MORE_POSTS = True
                print("no posts found")
                sleep(5)
            else:
                print("found posts")
                print('total posts found:', len(p))
                break
                
        for index, e in enumerate(p):
            action.scroll_by_amount(0, 120).perform()
            sleep(3)

            links = e.find_elements(By.XPATH, '//a[contains(@href, "/ads/about/")]')
            action.scroll_by_amount(0, -120).perform()
            sleep(3)

            if links:
                print("Found ads with '/ads/'")

            if not links:
                 links = e.find_elements(By.XPATH, '//a[@href="#"]')
                 print("trying to find href='#'")
                 sleep(3)

            wait = WebDriverWait(driver, 10)

            if not links:
                print("Can't find any ads post")

            if len(links):
                el = e.find_elements(By.XPATH, '//a[@role="link"]')
                print("looking into @role='link', found:", el)
                #driver.execute_script('arguments[0].scrollIntoView(true);', el)
                #print("scroll into view")
                #sleep(5)
                if len(el):
                    print("el links successfully retrieved!")
                    print("ready to move to element:", el[-1])
                    driver.execute_script('arguments[0].scrollIntoView(true);', el[-1])
                    print("scrolled into view")
                    sleep(10)
                    action.move_to_element(el[-1]).perform()
                    a = wait.until(EC.element_to_be_clickable(el[0]))
                    sleep(2)
                    if '/ads/' in e.get_attribute('innerHTML'):
                        like_count = e.find_elements(By.XPATH, './/span[@class="xt0b8zv x16hj40l"]')
                        if len(like_count):
                            only_int = [int(s) for s in like_count[0].text.split() if s.isdigit()]
                            if len(only_int):
                                print('like_count:', only_int[0])

            driver.execute_script('arguments[0].classList.add("seen");', e)

        # Calculate new scroll height and compare with last scroll height
        nh = driver.execute_script("return document.body.scrollHeight")
        if nh == lh:
            break
        lh = nh - 2
