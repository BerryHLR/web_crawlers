
# # "/hk/A1!en.assist.rtf?FROMCAPINDEX=Y"

# import requests
# from lxml import etree
# import json
# import io
# import time
# import os
# from selenium import webdriver

# download_dir = r'D:\Berry\UROP\2023 summer\hklaw_rtf'

# # 设置 Chrome 浏览器的下载选项
# chrome_options = webdriver.ChromeOptions()
# prefs = {'download.default_directory': download_dir}
# chrome_options.add_experimental_option('prefs', prefs)
# driver = webdriver.Chrome(options=chrome_options)

# def get_downloaded_file(download_url,download_dir, filename):
#     # 获得下载前的文件列表
#     before_download = set(os.listdir(download_dir))
#     driver.get(download_url)

#     # 等待文件下载
#     time.sleep(5)  
#     while True:
#         # 获取下载后的文件列表
#         after_download = set(os.listdir(download_dir))
#         # 查找新下载的文件
#         new_files = after_download - before_download
#         if new_files:
#             # 获取新下载的文件名
#             downloaded_file = new_files.pop()
#             # 定义新的文件路径（包含新的文件名）
#             new_file_path = os.path.join(download_dir, filename)
#             # 检查新的文件路径是否已存在，如果存在，则删除已存在的文件
#             if os.path.exists(new_file_path):
#                 os.remove(new_file_path)
#             # 重命名新下载的文件
#             os.rename(os.path.join(download_dir, downloaded_file), new_file_path)
#             return new_file_path  # 返回新的文件路径
#         time.sleep(1) 

# # /hk/A2!en.assist.rtf?FROMCAPINDEX=Y
# #download_urls = [f"https://www.elegislation.gov.hk/hk/A{i}!en.assist.rtf?FROMCAPINDEX=Y" for i in range(1,3)]
# download_urls =[f"https://www.elegislation.gov.hk/hk/cap{i}!en.assist.rtf?FROMCAPINDEX=Y" for i in range(1,3)]
# for i,download_url in enumerate(download_urls):
#     filename = "CAP" + str(i+1)

#     downloaded_file = get_downloaded_file(download_url,download_dir,filename)
#     print(f"The new downloaded file is: {downloaded_file}")

# driver.quit() # 关闭 Chrome 浏览器

import requests
import os

download_urls = [f"https://www.elegislation.gov.hk/hk/cap{i}!en.assist.rtf?FROMCAPINDEX=Y" for i in range(1,51)]
download_dir = r'D:/Berry/UROP/2023 summer/hklaw_rtf'
for i,download_url in enumerate(download_urls):
    filename = f"CAP{i+1}.rtf"  # 手动设置文件名和后缀名为rtf

    # 发送HTTP请求并下载文件
    response = requests.get(download_url)
    if response.ok:
        # 将文件保存到本地
        file_path = os.path.join(download_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded file saved at: {file_path}")
    else:
        print("Failed to download file.")