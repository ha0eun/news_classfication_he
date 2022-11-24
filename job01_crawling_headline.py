from bs4 import BeautifulSoup   # pip install beautifulsoup4
import requests    # pip install requests
import re
import pandas as pd    # pip install pandas
import datetime
import matplotlib.pyplot as plt   # pip install matplotlib


category =['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100' # 정치
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101' # 경제
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102' # 사회


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
df_titles = pd.DataFrame()
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers) # requests 응답
    # print(list(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')  # resp 요청을 BeautifulSoup로 html 문서형태로 바꿔줌
    # print(soup)
    title_tags = soup.select('.cluster_text_headline')  # 기사제목을 찾아서 리스트 형태로 보여줌
    # print(title_tags[0].text)  # 제목 1개만 찾음
    titles = []
    for title_tag in title_tags:  # 뉴스 제목만
        title = title_tag.text
        print(title)
        title = re.compile('[^가-힣]').sub(' ', title)  #('[^가-힣]') == 가-힣 한글 전체만 빼고 다 지워라/ ^ == 반전/  sub(' ', title) sub은 다 지워라
        print(title)                            # ('[^가-힣0-9a-zA-Z]') 한글, 숫자, 대소문자만 남기고 다빼라
        titles.append(title)  # 크롤링한 뉴스 제목이 들어감 titles에
    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles['category'] = category[i]   # 카테코리
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True) # 빈데이터 프레임에 합침. row = 자료를 합침
                                    # df_titles 여기에는 정치 카테고리 데이터가 들어가있음
    print(df_titles)
    print(df_titles.category.value_counts())  # 섹션 마다 다름
    df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
        datetime.datetime.now().strftime('%Y%m%d')), index=False)

