#파일 명:
#naver_headline_news_Politics_{}.csv
#('Politics', 'Economic', 'social', 'Culture', 'World', 'IT')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time


options = ChromeOptions()

options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = 'https://news.naver.com/section/100'
driver.get(url)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
for i in range(5):
    time.sleep(0.5)
    driver.find_element(By.XPATH, button_xpath).click()
time.sleep(5)

for i in range(1, 6): # 5회
    for j in range(1, 7): # 1부터 6까지
        time.sleep(0.5)
        title_path = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
        try: # 해당 경로가 없을 수도 있으니까 예외 처리를 위한 try-except 문
            title = driver.find_element(By.XPATH, title_path).text # 요소 찾기.text
            print(title)
        except:
            print('error', i, j)











# '//*[@id="_SECTION_HEADLINE_LIST_adhba"]/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[2]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[4]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[5]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[6]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[6]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[3]/div/a'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[4]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[6]/ul/li[4]/div/div/div[2]/a/strong'