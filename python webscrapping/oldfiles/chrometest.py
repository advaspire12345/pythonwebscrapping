
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyautogui

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")

driver.maximize_window()

title = driver.title
print(title)

driver.implicitly_wait(0.5)

sleep(1)

actions = ActionChains(driver)

element = driver.find_element(By.NAME, "q")

actions.move_to_element(element).click(element).perform

actions\
    .key_down(Keys.CONTROL)\
    .send_keys("n")\
    .key_up(Keys.CONTROL)\
    .perform()

print("send keys")

sleep(1)

driver.execute_script("document.body.style.zoom='200%';")

sleep(5)

driver.execute_script("document.body.style.zoom='100%';")
driver.execute_script("document.body.removeAttribute('style');")

sleep(10)

driver.close()

