
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
driver.get('https://acmp.ru')

login = driver.find_element(By.NAME, value='lgn')
login.clear()
login.send_keys('bot_pythonist')

password = driver.find_element(By.NAME, value='password')
password.clear()
password.send_keys('qwerty')

button = driver.find_element(By.CLASS_NAME, value='button')
button.send_keys(Keys.ENTER)


def checkACMP(task_id, code):
    driver.get(f'https://acmp.ru/index.asp?main=status&id_t={task_id}&id_mem=397031')
    last_res = (driver.find_element(By.CLASS_NAME, value='main').text.split('\n') + [''])[1]


    driver.get(f'https://acmp.ru/index.asp?main=task&id_task={task_id}')
    driver.find_element(By.CLASS_NAME, value='CodeMirror-code').click()
    for s in code.split('\n'):
        webdriver.ActionChains(driver).send_keys(s).perform()
        webdriver.ActionChains(driver).send_keys('\n').perform()
        webdriver.ActionChains(driver).send_keys(Keys.HOME).perform()

    Select(driver.find_element(By.NAME, 'lang')).select_by_index(1)

    driver.find_element(By.CLASS_NAME, value='button').click()

    while True:
        driver.get(f'https://acmp.ru/index.asp?main=status&id_t={task_id}&id_mem=397031')
        result = (driver.find_element(By.CLASS_NAME, value='main').text.split('\n') + 2*[])[1]
        if last_res != result:
            res = result.split(' ')
            if res[6] not in ['Waiting', 'Running', 'Compiling']:
                return ' '.join(res[6:res.index('')])
        sleep(1)
