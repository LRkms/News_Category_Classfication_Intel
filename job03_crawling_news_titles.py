#카테고리 'Politics', 'Economic', 'social', 'Culture', 'World', 'IT'
#16번 째 줄에 있는 카테고리를 변경 후 25번째 줄 숫자를 카테고리의 숫자로 변경 후 실행


from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
start = time.time()
category = 'Politics'

# Selenium 설정
options = ChromeOptions()
options.add_argument('lang=ko_KR')
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# BeautifulSoup으로 초기 헤드라인 수집
url = 'https://news.naver.com/section/100'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')

title_tags = soup.select('.sa_text_strong')
titles = []
for tag in title_tags:
    titles.append(tag.text)

# Selenium으로 추가 헤드라인 수집
driver.get(url)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
for i in range(30): #더보기 횟수
    time.sleep(0.5)
    try:
        driver.find_element(By.XPATH, button_xpath).click()
    except:
        print('error {category}')

for j in range(1, 200):
    for k in range(1, 7):
        time.sleep(0.5)
        title_path = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(j, k)
        try:
            title = driver.find_element(By.XPATH, title_path).text
            titles.append(title)
        except:
            print('error', j, k)

# DataFrame 생성 및 CSV 저장
df_titles = pd.DataFrame(titles, columns=['titles'])

# Politics 카테고리 CSV 파일로 저장 (헤드라인 제목만)
df_titles[['titles']].to_csv(
    './crawling_data/naver_headline_news_{}_{}.csv'.format(
        category, datetime.datetime.now().strftime('%Y%m%d')
    ),
    index=False
)

time.sleep(5)
end = time.time()
print("실행 시간:", end - start, "초")
'//*[@id="newsct"]/div[4]/div/div[1]/div[301]/ul/li[6]/div/div/div[2]/a/strong'#50번 더보기 마지막 헤드라인
'//*[@id="newsct"]/div[4]/div/div[1]/div[6]/ul/li[4]/div/div/div[2]/a/strong'