import os
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle


print('Authorization...')

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(desired_capabilities=caps, options=options)
driver.get('https://acmp.ru')

login = driver.find_element(By.NAME, value='lgn')
login.clear()
login.send_keys('bot_pythonist')

password = driver.find_element(By.NAME, value='password')
password.clear()
password.send_keys('qwerty')

button = driver.find_element(By.CLASS_NAME, value='button')
button.send_keys(Keys.ENTER)


def check_task(task_id):
    driver.get(f'https://acmp.ru/index.asp?main=status&id_t={task_id}&id_mem=397031')
    last_res = (driver.find_element(By.CLASS_NAME, value='main').text.split('\n') + [''])[1]

    driver.get(f'https://acmp.ru/index.asp?main=task&id_task={task_id}')
    driver.find_element(By.NAME, "fname").send_keys(os.getcwd() + "/input.py")
    driver.find_element(By.CLASS_NAME, value='button').click()

    while True:
        driver.get(f'https://acmp.ru/index.asp?main=status&id_t={task_id}&id_mem=397031')
        result = (driver.find_element(By.CLASS_NAME, value='main').text.split('\n') + 2*[])[1]
        if last_res != result:
            res = result.split(' ')
            if res[6] not in ['Waiting', 'Running', 'Compiling']:
                return ' '.join(res[6:res.index('')])
        sleep(1)


def get_task(task_id):
    link = f'https://acmp.ru/index.asp?main=task&id_task={task_id}'
    response = requests.get(link)
    if response.status_code == 200:

        response.encoding = 'cp1251'
        soup = BeautifulSoup(response.text, 'lxml')

        task_text = soup.find_all('p', class_='text')

        exemples = []
        for line in soup.find('table', class_='main').find_all('tr')[1:]:
            exemples.append([e.text for e in line.find_all('td')[1:]])

        limits = soup.find_all('i')[0].text
        hurd = int(limits[limits.rfind(':') + 2:limits.rfind('%')])
        level = sorted([hurd, 20, 25, 40, 70]).index(hurd)

        res = [soup.find_all('h1')[0].text, link, ''.join([t.text for t in task_text]),
               exemples, level, get_image(task_id), get_ans_task(task_id)]

        return res


def get_image(task_id):
    driver.get(f'https://acmp.ru/index.asp?main=task&id_task={task_id}')
    link = driver.find_elements(By.TAG_NAME, value='img')[-1].get_attribute('src')
    return link if 'id' in link else None


def get_ans_task(task_id):

    with open('ACMP_answers.txt', 'rb') as f:
        ansrs = pickle.load(f)

    if ansrs.get(task_id) is None:
        return None

    return f'https://raw.githubusercontent.com/AngelinaKhilman/algorithms/master/{ansrs[task_id]}'
