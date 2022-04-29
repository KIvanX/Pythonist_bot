import random

import aiogram.utils.markdown as fmt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os

header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'cookie': 'mos_id=CllGxlx+PS20pAxcIuDnAgA=; session-cookie=158b36ec3ea4f5484054ad1fd21407333c874ef0fa4f0c8e34387efd5464a1e9500e2277b0367d71a273e5b46fa0869a; NSC_WBS-QUBG-jo-nptsv-WT-443=ffffffff0951e23245525d5f4f58455e445a4a423660; rheftjdd=rheftjddVal; _ym_uid=1552395093355938562; _ym_d=1552395093; _ym_isad=2'
    }

print('Authorization in Informatics...')

caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(desired_capabilities=caps, options=options)
driver.get('https://informatics.msk.ru/')

login = driver.find_element(By.NAME, value='username')
login.clear()
login.send_keys('bot_pythonist')

password = driver.find_element(By.NAME, value='password')
password.clear()
password.send_keys('Qwerty(1')

button = driver.find_element(By.CLASS_NAME, value='btn-block')
button.send_keys(Keys.ENTER)


def check_task(task_id):
    driver.get(f'https://informatics.msk.ru/mod/statements/view.php?chapterid={task_id}')
    action = ActionChains(driver)

    action.move_to_element(driver.find_element(By.ID, "upload_button")).perform()
    driver.find_element(By.NAME, "file").send_keys(os.getcwd() + "/file.py")
    driver.find_element(By.ID, value='submit_button').click()

    driver.get('https://informatics.msk.ru/submits/view.php?user_id=719467#1')


check_task(1)


def get_task(task_id):
    req = requests.get(f'https://informatics.msk.ru/mod/statements/view.php?chapterid={task_id}', headers=header)

    if req.status_code == 200:
        # req.encoding = 'cp1251'
        soup = BeautifulSoup(req.text, 'lxml')
        task_text = ''
        for l in soup.find_all('section', class_='has-blocks mb-3'):
            task_text += fmt.quote_html(l.text)

        while task_text.find('\n\n\n') >= 0:
            task_text = task_text.replace('\n\n\n', '\n\n')

        return task_text[:task_text.find('Примеры')]
    else:
        return f'{req.status_code} error'
