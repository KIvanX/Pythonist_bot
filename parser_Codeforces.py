
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

print('Authorization...')

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(desired_capabilities=caps, options=options)
driver.get('https://codeforces.com/enter?back=%2F')

login = driver.find_element(By.NAME, value='lgn')
login.clear()
login.send_keys('KivanX')

password = driver.find_element(By.NAME, value='password')
password.clear()
password.send_keys('qwerty')

button = driver.find_element(By.CLASS_NAME, value='button')
button.send_keys(Keys.ENTER)

def check_task(task_id, code):
    return 'None'


def get_task(task_id):
    return 'None'


def get_ans_task(task_id):
    return 'None'
