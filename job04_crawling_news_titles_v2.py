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

# 카테고리
category_mapping  = {
    # 'Politics': '100',
    # 'Economic': '101', #button_xpath = '//*[@id="newsct"]/div[5]/div/div[2]'
    # 'Social': '102',
    # 'Culture': '103',
    # 'World': '104',
    'IT': '105'
}

# 모든 카테고리에 대해 반복
for category_name, category_code in category_mapping.items():
    start = time.time()
    print(f"===== {category_name} 카테고리 크롤링 시작 =====")
    
    # Selenium 설정
    options = ChromeOptions()
    options.add_argument('lang=ko_KR')
    options.add_argument('--headless')  # 브라우저 창 숨기기 (속도 향상)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # 네이버 뉴스 페이지로 이동
    url = f'https://news.naver.com/section/{category_code}'
    driver.get(url)
    
    # 제목을 저장할 리스트 초기화
    titles = []
    
    # 더보기 버튼 XPath
    button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
    
    
    # 더보기 클릭 횟수
    more_clicks = 100
    consecutive_errors = 0
    
    # 더보기 클릭
    for i in range(more_clicks):
        try:
            # 더보기 버튼이 보일 때까지 스크롤
            button = driver.find_element(By.XPATH, button_xpath)
            driver.execute_script("arguments[0].scrollIntoView();", button)
            time.sleep(1)
            button.click()
            print(f"더보기 {i+1}/{more_clicks}회 클릭 성공")
            consecutive_errors = 0  # 성공했으므로 에러 카운트 초기화
            
            # 10회마다 현재까지 수집된 건수 출력
            if (i+1) % 10 == 0:
                print(f"현재까지 {len(titles)}개의 제목 수집됨")
                
        except Exception as e:
            consecutive_errors += 1
            print(f"더보기 클릭 중 에러 발생 ({i+1}회): {category_name}")
            
            # 페이지 새로고침 시도
            if consecutive_errors == 2:
                print("페이지 새로고침 시도...")
                driver.refresh()
                time.sleep(2)
            
            # 5회 연속 에러 시 중단
            if consecutive_errors >= 5:
                print("연속 에러로 더보기 중단")
                break
                
            time.sleep(2)  # 에러 발생 시 더 오래 대기
    
    print("더보기 완료. 제목 수집 시작...")
    
    # div와 li 인덱스 범위를 조정 (더 많은 범위로 확장)
    for j in range(1, 701):  # div 범위 확장
        div_success = False
        
        for k in range(1, 7):
            try:
                # XPath 사용
                title_path = f'//*[@id="newsct"]/div[4]/div/div[1]/div[{j}]/ul/li[{k}]/div/div/div[2]/a/strong'
                title = driver.find_element(By.XPATH, title_path).text
                if title.strip():  # 빈 문자열이 아닌 경우에만 추가
                    titles.append(title)
                    div_success = True
                    
                    # 50개마다 출력
                    if len(titles) % 50 == 0:
                        print(f"현재 {len(titles)}개 제목 수집됨")
            except:
                pass
        
        # 아무것도 찾지 못했으면 5번 더 시도하고 종료
        if not div_success:
            # 마지막으로 발견된 div에서 5개 더 확인 후 종료
            empty_div_count = 1
            if empty_div_count >= 5:
                print(f"더 이상 제목을 찾을 수 없어 {j}번째 div에서 종료")
                break
            empty_div_count += 1
    
    # 중복 제거
    unique_titles = list(dict.fromkeys(titles))
    
    print(f"총 {len(unique_titles)}개 제목 수집 완료 (중복 제거 전: {len(titles)}, 후: {len(unique_titles)})")
    
    # DataFrame 생성 및 CSV 저장
    df_titles = pd.DataFrame(unique_titles, columns=['titles'])
    
    # CSV 파일로 저장
    file_path = f'./crawling_data/naver_headline_news_{category_name}_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
    df_titles.to_csv(file_path, index=False)
    
    print(f"{len(df_titles)}개의 고유 제목을 {file_path}에 저장 완료")
    
    # 브라우저 종료
    driver.quit()
    
    end = time.time()
    print(f"{category_name} 실행 시간: {end - start:.2f}초")
    print(f"===== {category_name} 카테고리 크롤링 완료 =====\n")
    
    # 카테고리 간 잠시 대기
    time.sleep(5)

print("모든 카테고리 크롤링 완료!")