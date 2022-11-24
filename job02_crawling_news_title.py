from selenium import webdriver      # pip install selenium
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category =['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# pages = [167, 377, 505, 71, 94, 73] # 페이지수 - page700을 하면 끝 페이지 알수 있음/ 1 페이지 당 20개 뉴스
# 데이터수가 차이가 많이 나면 수량을 맞춰 줘야함. 100페이지로 맞추고 , 적은 것들은 마지막 페이지 빼고 함(20개뉴스가 없을 수도 있어서)
pages = [101, 101, 101, 71, 94, 73]
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=2'

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
df_title = pd.DataFrame()
for i in range(0, 6):     # Section / 사회문화 (2, 4)
    titles = []
    for j in range(1, 11):     # page/  페이지는 1부터 시작, 마지막 페이지에는 뉴스 20개가 없을 수도 있어서 그 전 페이지까지 봐야함
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2)
        for k in range(1, 5): # x_path
            for l in range(1, 6):   # x_path
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
                try:
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
                except NoSuchElementException as e:
                    x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)  # 이미지가 없는 기사라 오류가 나서 다시 처리함
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
                except:
                    print('error')

        if j % 10 == 0:  # 10 페이지마다 저장됨
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[i]
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(category[i], j),
                            index = False)  # ex) crawling_data_{카테고리 정치}_{페이지 10마다 저장}
            titles = []

