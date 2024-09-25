import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# 保存电影数据到CSV文件的函数
def save_to_csv(movies, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'rating', 'quote', 'year', 'country', 'category', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)

# 抓取每一页电影信息的函数
def fetch_movie_data():
    movies = []
    for page in range(10):  # 豆瓣Top250有10页
        url = f'https://movie.douban.com/top250?start={page * 25}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取当前请求的时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for item in soup.find_all('div', class_='item'):
            title = item.find('span', class_='title').get_text()
            rating = item.find('span', class_='rating_num').get_text()
            quote = item.find('span', class_='inq').get_text() if item.find('span', class_='inq') else "N/A"
            info = item.find('p', class_='').get_text().strip().split('\n')[0]

            # 处理年份、国家、类型，避免 IndexError
            info_parts = info.split('/')
            year = info_parts[0].strip() if len(info_parts) > 0 else "Unknown"
            country = info_parts[1].strip() if len(info_parts) > 1 else "Unknown"
            category = info_parts[2].strip() if len(info_parts) > 2 else "Unknown"

            movies.append({
                'title': title,
                'rating': rating,
                'quote': quote,
                'year': year,
                'country': country,
                'category': category,
                'timestamp': timestamp  # 添加时间戳
            })

        print(f"Page {page + 1} scraped.")
        time.sleep(1)  # 为了避免过快请求导致被封，可以设置一个小延时

    return movies

# 主函数
if __name__ == "__main__":
    movies_data = fetch_movie_data()
    save_to_csv(movies_data, 'douban_top250_full.csv')
    print("全部数据已保存到 douban_top250_full.csv")
