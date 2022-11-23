from bs4 import BeautifulSoup   # pip install beautifulsoup4
import requests    # pip install requests
import re
import pandas as pd    # pip install pandas
import datetime
import matplotlib.pyplot as plt   # pip install matplotlib


category =['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

url = https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100  # 정치

df_titles = pd.DataFrame()
resp = requests.get(url)
print(resp)