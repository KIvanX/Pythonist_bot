
from selenium import webdriver
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

print('Authorization in Informatics...')

caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "eager"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(desired_capabilities=caps, options=options)


def get_task(task_id):
    driver.get(f'https://informatics.msk.ru/mod/statements/view.php?chapterid={task_id}')

    all_text = str(driver.find_element(value='region-main').text)
    all_text = all_text.replace(r'\\lt', '<').replace(r'\(', '').replace(r'\)', '')
    name = all_text.split('\n')[0]
    name = name[name.find('.')+2:]

    exemples_text = all_text[all_text.find('Примеры')+23: all_text.rfind('\n')]
    exemples_text = exemples_text.replace('входные данные\n', '_')
    exemples_text = exemples_text.replace('выходные данные\n', '_')
    exemples = exemples_text.split('_')
    exemples = [[exemples[i*2], exemples[i*2+1]] for i in range(len(exemples)//2)]

    # print(all_text)
    text = all_text.split('\n')[1:all_text.split('\n').index('Примеры')]
    for i, l in enumerate(text):
        if l in ['Входные данные', 'Выходные данные']:
            text[i] = '\n\n' + l + ':\n'
            text[i+1] = text[i+1]
    text = ' '.join(text)

    return name, text, exemples


# tasks, n, i = [], 0, 0
# while n < 300:
#     try:
#         name, text, exemples = get_task(i)
#         task = metod.Task(name, None, text, exemples, 3)
#         tasks.append(task)
#         print(n)
#         n += 1
#     except:
#         print('err', i)
#     i += 1
#
# with open('informatics_tasks.pkl', 'wb') as f:
#     pickle.dump(tasks, f)

# with open('informatics_tasks.pkl', 'rb') as f:
#     tasks = pickle.load(f)
#
# for i, t in enumerate(tasks):
#     print(f'{i+1}) {t.name}')
