import random

import aiogram.utils.markdown as fmt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

# print('Authorization...')
#
# caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "eager"
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(desired_capabilities=caps, options=options)
# driver.get('https://acmp.ru')
#
# login = driver.find_element(By.NAME, value='lgn')
# login.clear()
# login.send_keys('bot_pythonist')
#
# password = driver.find_element(By.NAME, value='password')
# password.clear()
# password.send_keys('qwerty')
#
# button = driver.find_element(By.CLASS_NAME, value='button')
# button.send_keys(Keys.ENTER)


def check_task(task_id, code):
    return 'Empty'
#     driver.get(f'https://acmp.ru/index.asp?main=status&id_t={task_id}&id_mem=397031')
#     last_res = (driver.find_element(By.CLASS_NAME, value='main').text.split('\n') + [''])[1]
#
#
#     driver.get(f'https://acmp.ru/index.asp?main=task&id_task={task_id}')
#     driver.find_element(By.CLASS_NAME, value='CodeMirror-code').click()
#     for s in code.split('\n'):
#         webdriver.ActionChains(driver).send_keys(s).perform()
#         webdriver.ActionChains(driver).send_keys('\n').perform()
#         webdriver.ActionChains(driver).send_keys(Keys.HOME).perform()
#
#     Select(driver.find_element(By.NAME, 'lang')).select_by_index(1)
#
#     driver.find_element(By.CLASS_NAME, value='button').click()
#
#     while True:
#         driver.get(f'https://acmp.ru/index.asp?main=status&id_t={task_id}&id_mem=397031')
#         result = (driver.find_element(By.CLASS_NAME, value='main').text.split('\n') + 2*[])[1]
#         if last_res != result:
#             res = result.split(' ')
#             if res[6] not in ['Waiting', 'Running', 'Compiling']:
#                 return ' '.join(res[6:res.index('')])
#         sleep(1)


def get_task(task_id):
    n = task_id if task_id is not None else random.randint(1, 1000)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'cookie': 'mos_id=CllGxlx+PS20pAxcIuDnAgA=; session-cookie=158b36ec3ea4f5484054ad1fd21407333c874ef0fa4f0c8e34387efd5464a1e9500e2277b0367d71a273e5b46fa0869a; NSC_WBS-QUBG-jo-nptsv-WT-443=ffffffff0951e23245525d5f4f58455e445a4a423660; rheftjdd=rheftjddVal; _ym_uid=1552395093355938562; _ym_d=1552395093; _ym_isad=2'
    }
    req = requests.get(f'https://informatics.msk.ru/mod/statements/view.php?chapterid={n}', headers=header)

    if req.status_code == 200:
        req.encoding = 'cp1251'
        soup = BeautifulSoup(req.text, 'lxml')
        task_text = soup.find_all('p', class_='text')
        # head = ' ' * 10 + soup.find_all('h1')[0].text
        # head = fmt.quote_html(head + '   ' + soup.find_all('i')[0].text + '\n')
        # text = head + '<i>' + fmt.quote_html(''.join([t.text for t in task_text])) + '</i>'
        # return text
        return f'Task {n} is not found'
    else:
        return f'Error req.status_code'
