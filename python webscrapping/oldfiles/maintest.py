# referenze:
# https://stackoverflow.com/questions/72754651/attributeerror-webdriver-object-has-no-attribute-find-element-by-xpath

from ast import Break
from pickle import NONE
from selenium import webdriver
import multiprocessing
from tkinter import *
from tkinter import ttk
from selenium.webdriver.support.ui import WebDriverWait
import tkinter.font as tkFont
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from time import sleep
import requests
import random
import urllib
import re
import os
import json
from PIL import Image
from io import BytesIO

root = Tk()
root.title('FB程序')
frm = ttk.Frame(root, padding=10)
frm.grid()
f = open("adspower.txt", encoding="utf-8")
f = f.readlines()
for i in range(len(f)):
    f[i] = f[i].replace('\n', '')

testing = False

if testing == True:
    quit()

def inizializer(all_data):
    command_data = all_data[0]
    account_number = 1
    try:
        account_number = int(all_data[6])
    except:
        pass
    ads_number = 0
    ads_id = f[ads_number]
    url = "http://local.adspower.com:50325/api/v1/browser/active?user_id=" + ads_id
    response = requests.request("GET", url, headers={}, data={})

    if response.json()['data']['status'] == 'Inactive':
        pass
    else:
        ads_number += 1
        ads_id = f[ads_number]
    open_url = "http://local.adspower.com:50325/api/v1/browser/start?user_id=" + ads_id
    close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id=" + ads_id
    for i in range(10):
        resp = requests.get(open_url).json()
        if resp["code"] != 0:
            sleep(0.5)
        else:
            break

    chrome_driver = resp["data"]["webdriver"].replace("driver.exe", "chromedriver.exe")

    options = Options()
    options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(chrome_driver, chrome_options=options)

    if all_data[1] == '' and all_data[2] == '':
        times = 0
    else:
        Data1 = int(all_data[1])
        Data2 = int(all_data[2])
        if Data1 != '':
            times = Data1
        if Data2 != '':
            times = Data2
        if Data1 == Data2:
            times = all_data[1]
        if Data1 != '' and Data2 != '':
            try:
                times = random.randint(Data1, Data2)
            except:
                times = random.randint(Data2, Data1)
    all_handles = driver.window_handles  # 获取到当前所有的句柄,所有的句柄存放在列表当中
    driver.switch_to.window(all_handles[1])
    # driver.switch_to_window(all_handles[1])
    # create action chain object
    action = ActionChains(driver)
    if command_data == 'account':
        DO_PAGE_LIKE = True
        DO_LIKES = True
        DO_SHARES = True
        DO_COMMENT = True
    else:
        DO_PAGE_LIKE = False
        DO_LIKES = False
        DO_SHARES = False
        DO_COMMENT = False
    # opzioni da mettere come interfaccia dopo
    if command_data == 'sponsor':
        NEWSFEED_SCRAPER = True
    else:
        NEWSFEED_SCRAPER = False
    # configure
    TIME_BETWEEN_EACH_LIKE = 2
    TIME_BETWEEN_EACH_SHARE = 2
    MSG_FOR_SHARE = [
        "Hi, we share this amazing post !",
        "have you see this ? like or comment it "
        "Do you need something like this?"
    ]

    MSG_FOR_COMMENTS = [
        ' Hi !',
        ' Hey',
        ' Whats Up?',
        ' OMG !'
    ]

    def send_data(data):
        url = 'https://onesplatform.com/api_insert_data.php'
        # api per screenshot:
        # image_url = 'https://onesplatform.com/api_insert_image.php'
        try:
            x = requests.post(url, json=data)
            print('response:', x.text, 'response end')
        except:
            pass

        return True

    df1 = pd.read_excel('pages.xlsx')
    df2 = pd.read_excel("posts.xlsx")

    def get_random_category():
        try:
            req = requests.get('https://onesplatform.com/api_get_all_category.php', verify=False, timeout=5)
            if req.ok:
                data = req.json()
                return data
        except:
            return [{"category_ID": "C1639059613", "title": "Property"},
                    {"category_ID": "C1644386246", "title": "Recruitment"},
                    {"category_ID": "C1649236426", "title": "Digital Marketing"},
                    {"category_ID": "C1652755672", "title": "Healthcare"},
                    {"category_ID": "C1656578687", "title": "Beauty"}]

    RANDOM_CAT_ID = {} #get_random_category()

    def find_save_elem(xpath):
        try:
            return driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def like_post(url):
        driver.get(url)
        toLike = driver.find_elements(By.XPATH, '//div[@role="article"]//div[@aria-label=\'Like\']')
        for i in range(10):
            try:
                driver.find_elements(By.XPATH, '//*[contains(text(),\'Like\')]')[1].click()
                break
            except:
                sleep(0.5)

                # action.click(e[0]).perform()
            # e[0].click()
            sleep(0.5)

    def share_post(url):
        driver.get(url)
        sleep(2)
        toShare = driver.find_elements(By.XPATH,
                                       '//div[@role="article"]//div[@aria-label=\'Send this to friends or post it on your Timeline.\']')

        # e = driver.find_elements(By.XPATH,
        # "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[8]/div/div[4]/div/div/div[1]/div/div[2]/div/div[3]/div/div[1]/div[2]/span")

        e = toShare
        if toShare:
            action.click(e[0]).perform()
            sleep(1)
            e = driver.find_elements(By.XPATH,
                                     '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div/div/div/span')
            if len(e):
                action.click(e[0]).perform()
                sleep(1)
                driver.switch_to.active_element.send_keys(random.choice(MSG_FOR_SHARE))
                e = driver.find_elements(By.XPATH,
                                         '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[3]/div[2]/div/div/div[1]/div/span')
                if len(e):
                    action.click(e[0]).perform()
        sleep(8)

    def comment_post(url):
        driver.get(url)
        sleep(0.5)
        e = None
        for i in range(10):
            try:
                e = driver.find_element(By.XPATH, '//div[@role="article"]//div[@aria-label=\'Leave a comment\']')
                break
            except:
                sleep(0.5)

        if e:
            # action.click(e).perform()
            e.send_keys(random.choice(MSG_FOR_COMMENTS))
            sleep(0.5)
            ActionChains(driver).key_down(Keys.RETURN).perform()
            ActionChains(driver).key_up(Keys.RETURN).perform()
        sleep(1)

    def do_page_like(url):
        driver.get(url)
        sleep(1)
        try:
            e = driver.find_element(By.XPATH, '//*[@aria-label=\'Liked\']')
            e.click()
        except:
            sleep(0.5)

    times2 = False
    times3 = 0
    post_times = 0.1
    try:
        post_times = int(E6.get())
    except:
        pass
    try:
        aa = int(E3.get())
        bb = int(E4.get())
        times2 = random.randint(aa, bb)
        times3 = times2 - round(times2 / 2)
    except:
        pass


    else:
        pass
    driver.get("https://www.facebook.com")
    random_times = False
    if times2:
        for index, row in df1.iteritems():
            for a, b in row.iteritems():
                if random_times == False:
                    random_times = random.sample(range(0, len(row.values)), len(row.values))
                if DO_LIKES:
                    like_post(row.values[random_times[a]])
                times2 -= 1
                sleep(post_times)
                if times2 < times3:
                    break

        random_times = False
        for index, row in df2.iteritems():
            if random_times == False:
                random_times = random.sample(range(0, len(row.values)), len(row.values))
            for a, b in row.iteritems():
                if DO_COMMENT:
                    comment_post(row.values[random_times[a]])
                if DO_SHARES:
                    share_post(row.values[random_times[a]])
                if DO_PAGE_LIKE:
                    do_page_like(row.values[random_times[a]])
                times2 -= 1
                sleep(post_times)
                if times2 < 0:
                    break

    else:
        for index, row in df1.iteritems():
            for a, b in row.iteritems():
                if DO_LIKES:
                    like_post(b)
                sleep(post_times)
        for index, row in df2.iteritems():
            for a, b in row.iteritems():
                if DO_COMMENT:
                    comment_post(b)
                if DO_SHARES:
                    share_post(b)
                if DO_PAGE_LIKE:
                    do_page_like(b)
                sleep(post_times)

    # try:
    #     e = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]').click()
    #     e = driver.find_element(By.ID,'email')
    #     e.send_keys(EMAIL)
    #     e = driver.find_element(By.ID, 'pass')
    #     e.send_keys(PWD)
    #     e = driver.find_element(By.NAME,'login')
    #     e.click()
    # except (NoSuchElementException,TimeoutException):
    #     pass

    POSTS = []
    # size =e.size
    # w, h = size['width'], size['height']
    NO_MORE_POSTS = False

    def do_screenshot(element):
        import string
        import secrets
        alphabet = string.ascii_letters + string.digits
        rand = ''.join(secrets.choice(alphabet) for i in range(32))
        # now that we have the preliminary stuff out of the way time to get that image :D
        location = element.location
        print('location: ', location)
        size = element.size
        png = driver.get_screenshot_as_png()  # saves screenshot of entire page
        # print(png)
        im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        hash_ = random.getrandbits(128)
        w, h = im.size
        # im_crop = im.crop((left, upper, right, lower))
        cropped = im.crop((left, right, top, bottom))
        # print(im)
        cropped.save(f'screenshot.png')  # saves new cropped image

    def get_file_content_chrome(uri):
        import base64
        result = driver.execute_async_script("""
        var uri = arguments[0];
        var callback = arguments[1];
        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        xhr.onload = function(){ callback(toBase64(xhr.response)) };
        xhr.onerror = function(){ callback(xhr.status) };
        xhr.open('GET', uri);
        xhr.send();
        """, uri)
        if type(result) == int:
            raise Exception("Request failed with status %s" % result)
        return base64.b64decode(result)

    def find_sponsored_posts(times):
        #
        only_int = []
        global share_count
        global comments_count
        #p = driver.find_elements(By.CSS_SELECTOR, "div[class='b6ax4al1']:not(.seen)")
        p = driver.find_elements(By.CSS_SELECTOR, "a[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']:not(.seen)")
        if not len(p):
            NO_MORE_POSTS = True
            print("no ads found")
            return True
        
        print("found posts (p), total:", len(p))
        for index, e in enumerate(p):
            # do_screenshot(e)
            # del p[index]
            action.scroll_by_amount(0, -120).perform()
            # driver.execute_script('arguments[0].scrollIntoView();', e)
            sleep(0.1)

            title = e.find_elements(By.XPATH, '//h4')
            links = e.find_elements(By.XPATH, "//a[contains(@href, '/ads/about/')]")
            if not links:
                links = e.find_elements(By.XPATH, "//a[@href='#']")
                sleep(1)
            wait = WebDriverWait(driver, 10)
            print("links found:", len(links))
            if len(links):
                el = e.find_elements(By.XPATH, '//a[@role="link"]')
                if len(el):
                    print("total el found: ", len(el))
                    action.move_to_element(el[0]).perform()
                    a = wait.until(EC.element_to_be_clickable(el[0]))
                    sleep(2)
                    if '/ads/' in e.get_attribute('innerHTML'):
                        like_count = e.find_elements(By.XPATH, './/span[@class="x16hj40l"]')
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
                            sleep(0.5)
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
                                    sleep(0.5)

                            if not has_embed:
                                # non ha il link embed
                                continue
                            for ii in range(10):
                                inp = driver.find_element(By.XPATH, '//input[@aria-label="Sample code input"]')
                                if inp.get_attribute('value') == '':
                                    sleep(0.5)
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
                                    sleep(1)
                                    # inp = driver.find_element(By.XPATH,
                                    #                           '//div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[1]/label/input')
                                except:
                                    sleep(0.5)
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
                            send_data(obj)
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

        print("now at line 567")

    print("i'm out of finding sponsored ads")

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
            sleep(SCROLL_PAUSE_TIME)

            find_sponsored_posts(times)
            # Calculate new scroll height and compare with last scroll height
            nh = driver.execute_script("return document.body.scrollHeight")
            if nh == lh:
                break
            lh = nh - 2


fontExample = tkFont.Font(family="Arial", size=16, weight="bold")
L1 = Label(frm, text="最小次数", font=fontExample).grid(column=0, row=3)
E1 = Entry(frm, font=fontExample)
E1.grid(column=1, row=3)
L2 = Label(frm, text="最大次数", font=fontExample).grid(column=2, row=3)
E2 = Entry(frm, font=fontExample)
E2.grid(column=3, row=3)

L3 = Label(frm, text="最小次数", font=fontExample).grid(column=0, row=0)
E3 = Entry(frm, font=fontExample)
E3.grid(column=1, row=0)
L4 = Label(frm, text="最大次数", font=fontExample).grid(column=2, row=0)
E4 = Entry(frm, font=fontExample)
E4.grid(column=3, row=0)

L6 = Label(frm, text="养号间隔(秒)", font=fontExample).grid(column=0, row=1)
E6 = Entry(frm, font=fontExample)
E6.grid(column=1, row=1)

L7 = Label(frm, text="账户数量", font=fontExample).grid(column=2, row=1)
E7 = Entry(frm, font=fontExample)
E7.grid(column=3, row=1)

ttk.Button(frm, text="抓取数据", command=lambda: sponsor_start()).grid(column=0, row=5)
ttk.Button(frm, text="养号", command=lambda: account_start()).grid(column=0, row=2)

if __name__ == '__main__':

    def sponsor_start():
        sponsor_data = ['sponsor', E1.get(), E2.get(), E3.get(), E4.get(), E6.get(), E7.get()]
        sponsor_process = multiprocessing.Process(target=inizializer, args=(sponsor_data,))
        sponsor_process.start()

    def account_start():
        account_data = ['account', E1.get(), E2.get(), E3.get(), E4.get(), E6.get(), E7.get()]
        account_process = multiprocessing.Process(target=inizializer, args=(account_data,))
        account_process.start()


    root.mainloop()


