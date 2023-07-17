from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys as k
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

print("NO_MORE_POST")

def find_sponsored_posts(times):
        #
        print("running line 59")
        only_int = []
        global share_count
        global comments_count
        print("finding sponsored ads")
        p = driver.find_elements(By.CSS_SELECTOR, "div[class='x15bjb6t x1qlqyl8 xjb2p0i xt0psk2 x9f619']:not(.seen)")
        
        print(p)

        if not len(p): 
            NO_MORE_POSTS = True
            print("can't find any post")
            return True
            
        for index, e in enumerate(p):
            # do_screenshot(e)
            print("can find some posts")
            # del p[index]
            action.scroll_by_amount(0, -120).perform()
            driver.execute_script('arguments[0].scrollIntoView();', e)
            time.sleep(0.1)

            title = e.find_elements(By.XPATH, './/h4')
            print("found a post title:", title)
            links = e.find_elements(By.XPATH, ".//a[@aria-label='Sponsored']")
            print("found a post link:", links)
            if not links:
                links = e.find_elements(By.XPATH, "//a[@href='#']")
                print("found an ads post with href='#'")
                time.sleep(1)
            wait = WebDriverWait(driver, 10)
            if len(links):
                el = e.find_elements(By.CSS_SELECTOR, 'span:nth-child(2) a[role="link"]')
                if len(el):
                    action.move_to_element(el[-1]).perform()
                    a = wait.until(EC.element_to_be_clickable(el[0]))
                    time.sleep(2)
                    if '/ads/' in e.get_attribute('innerHTML'):
                        like_count = e.find_elements(By.XPATH, './/span[@class="nnzkd6d7"]')
                        if len(like_count):
                            only_int = [int(s) for s in like_count[0].text.split() if s.isdigit()]
                            if len(only_int):
                                print('like count:', only_int[0])
                        share_count = e.find_elements(By.XPATH,
                                                      './/div[@class="dkzmklf5"]//span[contains(text(),"次分享")]')
                        if not len(share_count):
                            share_count = e.find_elements(By.XPATH,
                                                          './/div[@class="dkzmklf5"]//span[contains(text(),"shares")]')
                        if len(share_count):
                            share_count = re.findall(r'\d+', share_count[0].text)
                            if len(share_count):
                                print("SHARE COUNT:", share_count[0])
                        comments_count = e.find_elements(By.XPATH,
                                                         './/div[@class="dkzmklf5"]//span[contains(text(),"条评论")]')
                        if not len(comments_count):
                            comments_count = e.find_elements(By.XPATH,
                                                             './/div[@class="dkzmklf5"]//span[contains(text(),"comments")]')
                        if len(comments_count):
                            comments_count = re.findall(r'\d+', comments_count[0].text)
                            if len(comments_count):
                                print("COMMENTS COUNT:", comments_count[0])
                        # do_screenshot(e)
                        post_id = ''
                        post_link = ''
                        imgs = e.find_elements(By.XPATH, './/img')
                        imgs = [x.get_attribute('src') for x in imgs]

                        for i in imgs:
                            size_img = re.search('\d+x\d+', i)
                            if size_img:
                                size_img = size_img.group(0).split('x')
                                if len(size_img):
                                    if int(size_img[0]) > 200:
                                        # check if image is icon pick only cover
                                        imgs = [i]

                        if len(imgs) and imgs[0].startswith("data:image/svg+xml") or len(imgs) and 'emoji.php' in imgs[
                            0]:
                            # non inviare svg o icone(non servono), possono dare errore al salvataggio del post da parte di api
                            imgs = []

                        # cta random perchè gli elementi html di facebook proprio i tag sono random, non si puo prendere con precisione
                        cta = ['Apply Now', 'Book Now', 'Contact Us', 'Call Now', 'Download']
                        cta = random.choice(cta)

                        logo = e.find_elements(By.CSS_SELECTOR, 'span.nc684nl6 image')
                        fb_page = e.find_elements(By.XPATH, './/h4/span/a')

                        more_text = e.find_elements(By.XPATH, ".//div[text()[contains(., 'See more')]]")
                        if len(more_text):
                            driver.execute_script('arguments[0].click()', more_text[0])
                            time.sleep(0.5)
                        ad_msg = e.find_elements(By.CSS_SELECTOR, 'div[data-ad-preview="message"]')
                        menu_dots = e.find_elements(By.CSS_SELECTOR, 'div[aria-haspopup="menu"]')
                        if len(menu_dots):
                            # TODO:
                            # SOme posts are videos so embed option is not available
                            # VIDEOS are video id
                            '''
                            https://www.facebook.com/thelowdown/posts/pfbid02koYvnRYAKS5fsMjxdis2vfiGjw7WEK9EbkdAEH1ZNKKELFGKpxiZvWmUzivPTYwpl
                            '''
                            menu_elem = wait.until(EC.element_to_be_clickable(menu_dots[0]))
                            action.click(menu_elem).perform()
                            has_embed = False
                            has_video = False

                            # MOVE THIS IN SPONSORED PART, ONLY FOR TESTING
                            # THIS IS FOR VIDEOS
                            # VIDEO PART START
                            videos = e.find_elements(By.XPATH, './/video')
                            if len(videos):
                                has_video = True

                            # VIDEO PART END

                            for i in range(10):
                                try:
                                    embed = e.find_element(By.XPATH, "//span[text() = 'Embed']")
                                    embed.click()
                                    has_embed = True
                                    # inp = driver.find_element(By.XPATH,
                                    #                           '//div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[1]/label/input')
                                except:
                                    time.sleep(0.5)

                            if not has_embed:
                                # non ha il link embed
                                continue
                            for ii in range(10):
                                inp = driver.find_element(By.XPATH, '//input[@aria-label="Sample code input"]')
                                if inp.get_attribute('value') == '':
                                    time.sleep(0.5)
                                else:
                                    break

                            to_parse = urllib.parse.unquote(inp.get_attribute('value'), encoding='utf-8',
                                                            errors='replace')
                            if 'video.php' in to_parse:
                                post_link = re.search('href=([^&]*)', to_parse).group(1)
                                post_id = re.search('videos/([^/]*)', post_link).group(1)
                                has_video = True
                                print("VIDEO DETECTED URL:")
                                print(post_link)
                                print(post_id)

                            if 'posts/' in to_parse:
                                post_id = re.search('posts/([^&]*)', to_parse).group(1)
                                post_link = re.search('href=([^"]*)', to_parse).group(1)
                            if 'story_fbid=' in to_parse:
                                post_id = re.search('&id=([^&]*)', to_parse).group(1)
                                post_link = re.search('href=([^"]*)', to_parse).group(1)

                            close_btn = driver.find_elements(By.XPATH, '//*[@aria-label="Close"]')
                            if len(close_btn):
                                driver.execute_script("arguments[0].click();", close_btn[0])
                            # PAROLE CHIAVI INIZIO
                            action.click(menu_dots[0]).perform()

                            why = None
                            for i in range(10):
                                try:
                                    why = e.find_element(By.XPATH, "//span[text() = 'Why am I seeing this ad?']")
                                    why.click()
                                    time.sleep(1)
                                    # inp = driver.find_element(By.XPATH,
                                    #                           '//div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[1]/label/input')
                                except:
                                    time.sleep(0.5)
                            LIST_KEYWORDS_ONE = []
                            keywords_one = e.find_elements(By.XPATH,
                                                           '//div[@role="dialog"]//div[@data-visualcompletion="ignore-dynamic"]')
                            for i in keywords_one:
                                if len(i.text) < 60:
                                    LIST_KEYWORDS_ONE.append(i.text)
                            print("PARTE 1 PAROLE CHIAVI: ", LIST_KEYWORDS_ONE)

                        obj = {
                            'title': title[0].text if len(title) else '',
                            'category_ID': random.choice(RANDOM_CAT_ID)['category_ID'],
                            'cover_img': imgs[0] if len(imgs) else '',
                            'page_link': fb_page[0].get_attribute('href') if len(fb_page) else '',
                            'company_logo': logo[0].get_attribute('xlink:href') if len(logo) else '',
                            'media_type': 1,
                            'gallery_folder': '',
                            'video_type': 1 if has_video else 0,
                            'yt_url': '',
                            'vimeo_url': '',
                            'pdf_url': '',
                            'post_ID': post_id,
                            'post_link': post_link,
                            'fb_page': fb_page[0].text if len(fb_page) else '',
                            'cta': cta,
                            'languange': 'english',
                            'post_type': 'article',
                            'copywriting_text': ad_msg[0].text if len(ad_msg) else '',
                            'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'log_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'fb_like': only_int[0] if only_int and len(only_int) else '',
                            'fb_share': share_count[0] if len(share_count) else '',
                            'fb_comment': comments_count[0] if len(comments_count) else '',
                            'text1':','.join(LIST_KEYWORDS_ONE),
                            'text2':'',
                            'APIKEY': '0YocFmw1ubi0iANGhd19EaRFQzhju57vSPHQ3h2jz78',
                        }
                        print('test', obj)
                        POSTS.append(obj)
                        if not has_video:
                            pass
                        times -= 1

                        with open('sponsored_posts.json', 'w') as fi:
                            fi.write(json.dumps(POSTS))
                            fi.close()

                        close_btn = driver.find_elements(By.XPATH,'//*[@aria-label="Close"]')
                        if len(close_btn):
                            driver.execute_script("arguments[0].click();", close_btn[0])
                        if times == 0:
                            exit()
                    # aggiungiere le classi al post gia visto.
            driver.execute_script('arguments[0].classList.add("seen");', e)

SCROLL_PAUSE_TIME = random.randint(2,5)

e = driver.find_element(By.TAG_NAME, 'body')
e.click()

lh = driver.execute_script("return document.body.scrollHeight")

if NEWSFEED_SCRAPER:
    # Remove the top bar in case clicked wrongly during automation
    topbar = driver.find_elements(By.XPATH, '//*[@role="banner"]')
    if len(topbar):
        driver.execute_script('arguments[0].remove();', topbar[0])
    while not NO_MORE_POSTS:
        # Scroll down to bottom
        action.scroll_by_amount(0, 50).perform()
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        find_sponsored_posts(2)
        print("find sponsored posts again")

        # Calculate new scroll height and compare with last scroll height
        nh = driver.execute_script("return document.body.scrollHeight")
        if nh == lh:
            break
        lh = nh - 2

