# Updated Scrapper Function on 17th July 2023
# Remove redundant element
# User Interface changed to Customtkinter Modern Design

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
from time import sleep
import requests
import random
import urllib
import re
import json
from PIL import Image
from io import BytesIO
import pyautogui as pag
import base64

# root = Tk()
# root.title('FB Scrapping Tool')
# frm = ttk.Frame(root, padding=10)
# frm.grid()

testing = False
zoom_ratio = 0
orig_height = 0
len_keywords = 0
len_keywords_2 = 0

if testing == True:
    quit()

def inizializer(scrap_data):

    PATH = r"C:\Users\khsra\Desktop\python webscrapping\chromedriver\chromedriver.exe"
    websitePath = "https://www.facebook.com/"
    # USERNAME = "leehoiching22@gmail.com"
    # PASSWORD = "OPLeHoCi!735@"

    # USERNAME = "liewkokkheong@gmail.com"
    # PASSWORD = "ONESLiKoKh!4457@"

    USERNAME = scrap_data[0]
    PASSWORD = scrap_data[1]

    print(PATH)
    print(USERNAME)
    print(PASSWORD)

    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(executable_path = PATH, chrome_options = options)

    driver.get(websitePath)
    driver.maximize_window()

    email = driver.find_element(By.ID, "email")
    email.send_keys(USERNAME)
    password = driver.find_element(By.ID, "pass")
    password.send_keys(PASSWORD)
    sleep(1)
    password.send_keys(Keys.RETURN)

    print(driver.current_url)
    sleep(1)

    action = ActionChains(driver)

    driver.get("https://www.facebook.com/")

    action = ActionChains(driver)

    # Only Scrap Ads posts
    NEWSFEED_SCRAPER = True

    def send_data(type, data):
               
        if type == 'data':
            # API link for data insert
            url = 'https://onesplatform.com/api_insert_data.php'
            print('Sending Data through API')
            try:
                x = requests.post(url, json=data)
                if x.text not in ['2','3','4']:
                    print('Success inserted data:', x.text)
                    return x.text
                elif x.text == '2':
                    print('Response: 2, Failed to Insert Data')
                elif x.text == '3':
                    print('Response: 3, Incomplete Data POST')
                elif x.text == '4':
                    print('Response: 4, Invalid API Key')
            except:
                pass

        elif type == 'image':
            # API link for inserting image
            image_url = 'https://onesplatform.com/api_insert_image.php'
            try:
                x = requests.post(image_url, json=data)
                if x.text not in ['2','3','4']:
                    print('Images inserted successfully')
                elif x.text == '2':
                    print('Response: 2, Failed to Insert Data')
                elif x.text == '3':
                    print('Response: 3, Incomplete Data POST')
                elif x.text == '4':
                    print('Response: 4, Invalid API Key')
            except:
                pass

        return 'unsuccessful'

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

    # RANDOM_CAT_ID = get_random_category()

    RANDOM_CAT_ID = [{"category_ID": "C1639059613", "title": "Property"},
                    {"category_ID": "C1644386246", "title": "Recruitment"},
                    {"category_ID": "C1649236426", "title": "Digital Marketing"},
                    {"category_ID": "C1652755672", "title": "Healthcare"},
                    {"category_ID": "C1656578687", "title": "Beauty"}]

    POSTS = []

    NO_MORE_POSTS = False

    def do_screenshot(element, save_file):
        global orig_height
        global len_keywords
        global len_keywords_2
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

        print('location x:', location['x'], 'location y:', location['y'])
        print('zoom width:', size['width'],', zoom height:', size['height'])

        # default settings 
        top = 2
        left = 580
        adj_width = size['width'] + 150
        adj_height = size['height'] + 150
        # when screenshooting the 'why am I seeing this ad?'

        if 'why_ads' in save_file:

            if len_keywords > 2:
                top = 180
            else:
                top = 230

            left = 605
            adj_width = size['width'] + 140
            adj_height = 112 + (67 * (len_keywords - 1))
            print('keywords length:',len_keywords)

            if 'why_ads_more' in save_file:
                top = 2
                adj_height = 880

        elif 'post' in save_file or 'copywriting' in save_file:

            # When screenshooting the ads post
            # when size is 100%
            top = 2

            if orig_height < 696:
                if save_file == 'post':
                    adj_width = size['width'] + 150
                    adj_height = size['height'] + 150
                    left = 580
                elif save_file == 'copywriting':
                    adj_width = size['width'] + 150
                    adj_height = size['height'] + 150
                    left = 580
                # Class = 'x78zum5 xdt5ytf xz62fqu x16ldp7u'

            # when size is 67%
            elif orig_height > 696 and orig_height < 834:
                adj_width = 560
                adj_height = int(size['height'] * 0.794)
                if adj_height > 880:
                    adj_height = 880
                left = 667

            # when size is 50%
            else:
                adj_width = 430
                adj_height = int(size['height'] * 0.605)
                if adj_height > 880:
                    adj_height = 880
                left = 735

        right = left + adj_width
        bottom = top + adj_height
        hash_ = random.getrandbits(128)
        w, h = im.size
        # im_crop = im.crop((left, upper, right, lower))
        print('x1:', left, ', y1:', top, ', x2:', right, ', y2:', bottom)
        print('width:', adj_width, ', height:', adj_height)
        cropped = im.crop((left, top, right, bottom))
        # print(im)
        cropped.save(f'{save_file}.png')  # saves new cropped image

    def upload_image(image):

        key_imgbb = "9f34c5da5538225aaa7de26a286f007b"

        with open(image, "rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": key_imgbb,
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)

        data = json.loads(res.text)

        return data['data']['url']

    def download_image(image_list):

        img_pkg = []

        for i, image in enumerate(image_list):
            
            try:
                img_data = requests.get(image).content
                with open('image{i}.jpg'.format(), 'wb') as handler:
                    handler.write(img_data)
                img_pkg.append('image{i}.jpg')
            except:
                sleep(0.5)
                continue

        return img_pkg

    def setup_photos(img_list):

        image_url_list = []
        img_pkg = download_image(img_list)

        for i, image_name in enumerate(img_pkg):
            try:
                image_url = upload_image(image_name)
                image_url_list.append(image_url)
            except:
                sleep(0.5)
                continue

        return image_url_list

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

    def auto_size(element):

        check_size = element.size
        print(check_size['height'])
        global zoom_ratio

        if check_size['height'] < 696:
            zoom_ratio = 0
        elif check_size['height'] > 696 and check_size['height'] < 834:
            zoom('out', 4)
            zoom_ratio = 4
        elif check_size['height'] > 834 and check_size['height'] < 1127:
            zoom('out', 5)
            zoom_ratio = 5
        else:
            zoom('out', 6)
            zoom_ratio = 6

    def zoom(action, time):
        
        for i in range(time):
            if action == 'out':
                pag.hotkey('ctrl', '-')
            if action == 'in':
                pag.hotkey('ctrl', '+')

    def find_sponsored_posts(times):
        #
        only_int = []
        global share_count
        global comments_count
        global orig_height
        LIST_KEYWORDS_TWO = []
        why_box = []
        photos = []
        why_image = ''

        #p = driver.find_elements(By.CSS_SELECTOR, "div[class='b6ax4al1']:not(.seen)")
        p = driver.find_elements(By.CSS_SELECTOR, "div[class='x1lliihq']:not(.seen)")
        if not len(p):
            NO_MORE_POSTS = True
            print("no ads found")
            return True
        for index, e in enumerate(p):
            # do_screenshot(e)
            print("found posts: ", len(p))
            # del p[index]
            action.scroll_by_amount(0, -120).perform()
            # driver.execute_script('arguments[0].scrollIntoView();', e)
            sleep(0.1)

            title = e.find_elements(By.XPATH, './/h4')
            links = e.find_elements(By.XPATH, ".//a[@aria-label='Sponsored']")
            if not links:
                links = e.find_elements(By.XPATH, "//a[@href='#']")
                sleep(1)
            wait = WebDriverWait(driver, 10)
            if len(title):
                print("found ads:", len(links), "and title:", title[0].text)
            if len(links):
                el = e.find_elements(By.CSS_SELECTOR, 'span:nth-child(2) a[role="link"]')
                print("found role link:", len(el))
                if len(el):
                    action.move_to_element(el[-1]).perform()
                    driver.execute_script('arguments[0].scrollIntoView();', el[-1])
                    print("moving to element")
                    sleep(1)
                    a = wait.until(EC.element_to_be_clickable(el[0]))
                    print(e.get_attribute('innerHTML')[0])
                    sleep(1)
                    
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
                                        # check if image is icon, pick only cover
                                        imgs = [i]

                        if len(imgs) and imgs[0].startswith("data:image/svg+xml") or len(imgs) and 'emoji.php' in imgs[0]:

                            # do not send svg or icons, it will give error when sending the post with api key
                            imgs = []

                        if imgs:
                            photos = setup_photos(imgs)

                        # CTA Random choose from below
                        cta = ['Apply Now', 'Book Now', 'Contact Us', 'Call Now', 'Download']
                        cta = random.choice(cta)

                        logo = e.find_elements(By.CSS_SELECTOR, 'span.nc684nl6 image')
                        fb_page = e.find_elements(By.XPATH, './/h4/span/a')
                        sleep(0.5)

                        driver.execute_script('arguments[0].scrollIntoView();', el[-1])
                        menu_dots = e.find_elements(By.CSS_SELECTOR, 'div[aria-haspopup="menu"]')
                        if len(menu_dots):
                            # TODO:
                            # SOme posts are videos so embed option is not available
                            # VIDEOS are video id

                            global len_keywords
                            global len_keywords_2

                            menu_elem = wait.until(EC.element_to_be_clickable(menu_dots[0]))

                            #check the size of post   
                            #auto_size(e)
                            orig_height = e.size['height']
                            print("orig_height:", orig_height)

                            if orig_height < 696:
                                pass

                            elif orig_height > 696 and orig_height < 834:
                                print('After Zoom Out:')
                                zoom('out', 4)

                            else:
                                print('After Zoom Out:')
                                zoom('out', 5)

                            driver.execute_script('arguments[0].scrollIntoView();', el[-1])
                            action.move_to_element(menu_dots[0])

                            #for 100% view
                            if orig_height < 696:

                                action.scroll_by_amount(0, -35) 

                            #for view that is less than 67%
                            else:

                                action.scroll_by_amount(0, -20) 

                            sleep(1)
                            print("moving to menu dot")
                            action.click(menu_elem).perform()
                            sleep(0.1)
                            action.click(menu_elem).perform()
                            sleep(0.1)
                            print("clicking the menu dot")
                            sleep(1)

                            do_screenshot(e, 'post')
                            print("doing screenshot")
                            sleep(1)

                            first_look_img = upload_image('post.png')

                            #zoom('in', zoom_ratio)
                            if orig_height < 696:
                                pass

                            elif orig_height > 696 and orig_height < 834:
                                zoom('in', 4)

                            else:
                                zoom('in', 5)

                            driver.execute_script('arguments[0].scrollIntoView();', el[-1])
                            action.move_to_element(menu_dots[0])
                            action.click(menu_elem).perform()
                            sleep(0.5)
                            print("clicking the menu dot")
                            has_embed = False
                            has_video = False

                            # MOVE THIS IN SPONSORED PART, ONLY FOR TESTING
                            # THIS IS FOR VIDEOS
                            # VIDEO PART START
                            videos = e.find_elements(By.XPATH, './/video')
                            if len(videos):
                                has_video = True

                            # VIDEO PART END

                            for i in range(5):
                                try:
                                    embed = e.find_element(By.XPATH, "//span[text() = 'Embed']")
                                    embed.click()
                                    has_embed = True
                                    # inp = driver.find_element(By.XPATH,
                                    #                           '//div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[1]/label/input')
                                except:
                                    sleep(0.5)

                            if not has_embed:
                                # no link embed
                                action.move_to_element(menu_dots[0])
                                action.click(menu_elem).perform()

                            if has_embed:
                                for ii in range(5):
                                    try:
                                        inp = driver.find_element(By.XPATH, '//input[@aria-label="Sample code input"]')
                                        if inp.get_attribute('value') == '':
                                            sleep(0.5)
                                        else:
                                            break
                                    except:
                                        sleep(0.5)
                            
                            to_parse = ''

                            if has_embed:
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
                            
                            close_btn = e.find_elements(By.XPATH, '//*[@aria-label="Close"]')
                            
                            if len(close_btn):
                                close_btn = wait.until(EC.element_to_be_clickable(close_btn[0]))
                                action.click(close_btn).perform()
                                sleep(1)

                            action.click(menu_dots[0]).perform()

                            # Keywords starts

                            why = None
                            for i in range(10):
                                try:
                                    why = e.find_element(By.XPATH, "//span[text() = 'Why am I seeing this ad?']")
                                    why.click()
                                    sleep(1)
                                    why_box = e.find_element(By.XPATH,'//div[@role="dialog"]')
                                
                                except:
                                    sleep(0.5)

                            LIST_KEYWORDS_ONE = []
                            keywords_one = e.find_elements(By.XPATH,
                                                           '//div[@role="dialog"]//div[@data-visualcompletion="ignore-dynamic"]')
                            for i in keywords_one:
                                if len(i.text) < 60:
                                    LIST_KEYWORDS_ONE.append(i.text)
                            print("PART 1 KEYWORDS: ", LIST_KEYWORDS_ONE)

                            len_keywords = len(LIST_KEYWORDS_ONE)

                            action.scroll_by_amount(0, 20) 

                            if why != None:

                                do_screenshot(why_box, "why_ads")
                                sleep(1)

                                if 'more' in LIST_KEYWORDS_ONE[0]:
                                    action.click(keywords_one[0]).perform()
                                    sleep(1)
                                    LIST_KEYWORDS_TWO = []
                                    keywords_one = e.find_elements(By.XPATH,
                                                                '//div[@role="dialog"]//div[@data-visualcompletion="ignore-dynamic"]')
                                    for i in keywords_one:
                                        if len(i.text) < 60:
                                            keyword_text = i.text.split('\n')[0]
                                            LIST_KEYWORDS_TWO.append(keyword_text)

                                    while "" in keyword_text:
                                        keyword_text.remove("")

                                    print("PART 2 KEYWORDS: ", LIST_KEYWORDS_TWO)

                                    len_keywords_2 = len(LIST_KEYWORDS_TWO)
                                    sleep(3)

                                    if len_keywords_2 > 6:
                                        action.scroll_by_amount(0, 100)
                                        sleep(3)

                                    why = None
                                    for i in range(10):
                                        try:
                                            why = e.find_element(By.XPATH, "//span[text() = 'Why am I seeing this ad?']")
                                            why.click()
                                            sleep(1)
                                            why_box = e.find_element(By.XPATH,'//div[@role="dialog"]')
                                
                                        except:
                                            sleep(0.5)

                                    do_screenshot(why_box, "why_ads_more")
                                    sleep(3)

                            action.click(menu_dots[0]).perform()

                            why_image = upload_image('why_ads.png')

                            sleep(3)
                        
                        more_text = e.find_elements(By.XPATH, ".//div[text()[contains(., 'See more')]]")

                        if len(more_text):
                            driver.execute_script('arguments[0].click()', more_text[0])
                            sleep(0.5)

                        for i in range(10):
                            try:
                                print('locating copywriting box')
                                copywriting_box = e.find_element(By.XPATH,'.//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"]')
                            except:
                                sleep(0.5)
                        
                        sleep(1)
                        if copywriting_box:
                            print("Copywriting box found, height:", copywriting_box.size['height'])
                        do_screenshot(copywriting_box, 'copywriting')

                        ad_msg = e.find_elements(By.CSS_SELECTOR, 'div[data-ad-preview="message"]')

                        page_link = fb_page[0].get_attribute('href') if len(fb_page) else ''

                        if page_link != '':
                            page_link = page_link.split('?')[0]

                        obj = {
                            'title': title[0].text if len(title) else '',
                            'cover_img': first_look_img,
                            # 'cover_img': imgs[0] if len(imgs) else '',
                            'fb_page': fb_page[0].text if len(fb_page) else '',
                            'video_type': 1 if has_video else 0,
                            'yt_url': '',
                            'vimeo_url': '',
                            'post_ID': post_id,
                            'post_link': post_link,
                            'page_link': page_link,
                            'cta': cta,
                            'copywriting_img':'',
                            'copywriting_text': ad_msg[0].text if len(ad_msg) else '',
                            'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'fb_like': only_int[0] if only_int and len(only_int) else '',
                            'fb_share': share_count[0] if len(share_count) else '',
                            'fb_comment': comments_count[0] if len(comments_count) else '',
                            'Category_ID': 0,
                            'APIKEY': 'RARazPnC2z47HB1uw962y8uI9AL5nDCQdXzDgqwgMt'

                            # Extra data                    
                            
                            # 'company_logo': logo[0].get_attribute('xlink:href') if len(logo) else '',
                            # 'media_type': 1,
                            # 'gallery_folder': '',
                            # 'pdf_url': '',
                            # 'languange': 'english',
                            # 'post_type': 'article',
                            # 'log_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            # 'text1':'Keywords 1:'.join(LIST_KEYWORDS_ONE),
                            # 'text2':'Keywords 2:'.join(LIST_KEYWORDS_TWO),

                        }

                        obj_img = {
                            'data_ID':'',
                            'img_url':'',
                            'type': '',
                            'APIKEY': 'RARazPnC2z47HB1uw962y8uI9AL5nDCQdXzDgqwgMt'
                        }

                        POSTS.append(obj)
                        if not has_video:
                            pass
                            # send_data('data', obj)
                            # print('Send Data through API')
                            # sleep(3)
                        
                        print(POSTS[0])
                        data_ID = send_data('data', POSTS[0])
                        sleep(3)
                        print("data_ID recorded:", data_ID)

                        # Upload image for First Look (First Look = 1)
                        if data_ID != 'unsuccessful':

                            # with open("post.png", "rb") as image_file:
                            #     encoded_img = base64.b64encode(image_file.read())

                            obj_img['data_ID'] = data_ID
                            obj_img['img_url'] = first_look_img
                            obj_img['type'] = '1'     # First look = 1 , Settings = 2, Photos = 3
                            send_data('image', obj_img)

                        # Upload image for Settings (Setting = 2)
                            obj_img['img_url'] = why_image
                            obj_img['type'] = '2'     # First look = 1 , Settings = 2, Photos = 3
                            send_data('image', obj_img)
                            print("Setting photo uploaded successfully!")

                        # Upload image for Image Gallery (Photos = 3)
                            if photos:
                                for i, photo in enumerate(photos):
                                    obj_img['img_url'] = photo
                                    obj_img['type'] = '3'     # First look = 1 , Settings = 2, Photos = 3
                                    send_data('image', obj_img)

                        times -= 1

                        with open('sponsored_posts.json', 'w') as fi:
                            fi.write(json.dumps(POSTS))
                            fi.close()

                        close_btn = driver.find_elements(By.XPATH,'//*[@aria-label="Close"]')
                        if len(close_btn):
                            driver.execute_script("arguments[0].click();", close_btn[0])
                        if times == 0:
                            exit()

            # Add a class to the post 'already seen'        
            driver.execute_script('arguments[0].classList.add("seen");', e)

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

            find_sponsored_posts(50)
            # Calculate new scroll height and compare with last scroll height
            nh = driver.execute_script("return document.body.scrollHeight")
            if nh == lh:
                break
            lh = nh - 2


# fontExample = tkFont.Font(family="Arial", size=16, weight="bold")
# L1 = Label(frm, text="最小次数", font=fontExample).grid(column=0, row=3)
# E1 = Entry(frm, font=fontExample)
# E1.insert(0, 10)
# E1.grid(column=1, row=3)
# L2 = Label(frm, text="最大次数", font=fontExample).grid(column=2, row=3)
# E2 = Entry(frm, font=fontExample)
# E2.insert(0, 10)
# E2.grid(column=3, row=3)

# L3 = Label(frm, text="最小次数", font=fontExample).grid(column=0, row=0)
# E3 = Entry(frm, font=fontExample)
# E3.grid(column=1, row=0)
# L4 = Label(frm, text="最大次数", font=fontExample).grid(column=2, row=0)
# E4 = Entry(frm, font=fontExample)
# E4.grid(column=3, row=0)

# L6 = Label(frm, text="养号间隔(秒)", font=fontExample).grid(column=0, row=1)
# E6 = Entry(frm, font=fontExample)
# E6.grid(column=1, row=1)

# L7 = Label(frm, text="账户数量", font=fontExample).grid(column=2, row=1)
# E7 = Entry(frm, font=fontExample)
# E7.grid(column=3, row=1)

# ttk.Button(frm, text="抓取数据", command=lambda: sponsor_start()).grid(column=0, row=5)
# ttk.Button(frm, text="养号", command=lambda: account_start()).grid(column=0, row=2)

# L8 = Label(frm, text="Username", font=fontExample).grid(column=0, row=6)
# E8 = Entry(frm, font=fontExample)
# E8.grid(column=1, row=6)

# if __name__ == '__main__':

#     def sponsor_start():
#         sponsor_data = ['sponsor', E1.get(), E2.get(), E3.get(), E4.get(), E6.get(), E7.get()]
#         sponsor_process = multiprocessing.Process(target=inizializer, args=(sponsor_data,))
#         sponsor_process.start()

#     def account_start():
#         account_data = ['account', E1.get(), E2.get(), E3.get(), E4.get(), E6.get(), E7.get()]
#         account_process = multiprocessing.Process(target=inizializer, args=(account_data,))
#         account_process.start()

#     root.mainloop()


