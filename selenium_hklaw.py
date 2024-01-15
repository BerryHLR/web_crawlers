from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import os
import re
import sys
from selenium.common.exceptions import NoSuchElementException

bro = webdriver.Chrome() #executable='D:\Berry\py\chromedriver-win64\chromedriver.exe'
data = []
download_dir = r'D:/Berry/UROP/2023 summer/hklaw_rtf'

for i in range(221,235):
    url = "https://www.elegislation.gov.hk/index/chapternumber/others?START_ENTRIES=Y&TYPE=1&TYPE=2&TYPE=3&LANGUAGE=E"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    bro.get(url)
    sleep(1)
    all_button = WebDriverWait(bro, 40).until(EC.element_to_be_clickable((By.ID, 'all')))
    sleep(3)
    all_button.click()
    sleep(3)
    download_button = WebDriverWait(bro, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.grid-link.grid-show-all')))
    sleep(3)
    download_button.click()
    titles = WebDriverWait(bro, 40).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@href="/hk/cap1"]' )))
    sleep(5)
    for title in titles:
        title = bro.find_element(By.XPATH,f'//a[@href="/hk/cap{i}"]')
        title = title.text
        title = f"CAP{i} : " + title 
        print(title)


    bro.get(f'https://www.elegislation.gov.hk/hk/cap{i}')
    sleep(4)
    try:
        divs = WebDriverWait(bro, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='PreviewWrapper']" )))
        text = ''.join([div.text for div in divs])
        #print(text)

        # 定义一个正则表达式，匹配所有非中文字符
        pattern = re.compile(r'[^\u4e00-\u9fff]+')

        # 使用正则表达式匹配所有非中文字符，并将它们连接成一个字符串
        english_text = ''.join(pattern.findall(text))
        dictionary = {title: english_text}
        data.append(dictionary)
        print(f"cap{i} has done.")
    # assume that bro is a WebDriver instance
    except NoSuchElementException:
        # if the element is not found, print an error message and continue to the next iteration
        print(f"Element not found for cap{i}, skipping...")
        continue

#new_data = [{"text": f"{k}:{v}"} for d in data for k, v in d.items()]
json_data = json.dumps(data,indent=4) #, ensure_ascii=False, separators=(" ", " "))
json_data = json_data.replace("\\n", " ").replace("\\t", " ").replace('\\u', ' ')
#print(json_data)
# 保存 JSON 数据到文件
with open(os.path.join(download_dir, "data动态cap221-234含标题.json"), 'w', encoding='utf-8') as f:
    f.write(json_data)
bro.quit()
