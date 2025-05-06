import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_top250_movies(save_path):
    base_url = 'https://movie.douban.com/top250'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    idxs = []
    movies = []

    count = 1
    for page in range(10):  # 获取前10页的结果
        url = f'{base_url}?start={page * 25}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        movie_list = soup.find_all('div', class_='hd')

        for movie in movie_list:
            title = movie.a.span.text
            idxs.append(count)
            movies.append(title)
            count += 1
    top_250 = {'序号': idxs, '电影': movies}
    df = pd.DataFrame(top_250, index=None)
    df.to_csv(save_path, encoding='utf-8-sig', index=False)


get_top250_movies(r'F:\Top250_Douban.csv')
