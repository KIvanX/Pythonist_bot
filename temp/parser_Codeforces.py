
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.121 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'cookie': 'mos_id=CllGxlx+PS20pAxcIuDnAgA=; '
                  'session-cookie'
                  '=158b36ec3ea4f5484054ad1fd21407333c874ef0fa4f0c8e34387efd5464a1e9500e2277b0367d71a273e5b46fa0869a; '
                  'NSC_WBS-QUBG-jo-nptsv-WT-443=ffffffff0951e23245525d5f4f58455e445a4a423660; rheftjdd=rheftjddVal; '
                  '_ym_uid=1552395093355938562; _ym_d=1552395093; _ym_isad=2 '
    }

print('Authorization in Codeforces...')

caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(desired_capabilities=caps, options=options)


def get_task(task_id):
    driver.get(f'https://codeforces.com/problemset/problem/{task_id}/A')

    all_text = str(driver.find_element(By.CLASS_NAME, value='problem-statement').text)
    all_text = all_text.replace(r'\\lt', '<').replace(r'\(', '').replace(r'\)', '')

    name = all_text.split('\n')[0]
    name = name[name.find('.')+2:]

    exemples = all_text[all_text.find('Примеры')+8:]
    exemples = exemples.replace('входные данные\nСкопировать\n', '_').replace('выходные данные\nСкопировать\n', '_')
    exemples = exemples.split('_')[1:]
    exemples = [[exemples[i*2], exemples[i*2+1]] for i in range(len(exemples)//2)]

    text = all_text.split('\n')
    text = '\n'.join(text[5:text.index('Примеры')])

    return name, text, exemples
