
import requests
from bs4 import BeautifulSoup
import pandas as pd

table_head = ['car','lowest_price','highest_price','img_url']


def get_content(request_url):
    # 得到页面的内容
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=headers, timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup


def content_analysis(soup):
    global table_head
    df = pd.DataFrame(columns=table_head)
    # 获得目标内容
    table = soup.find('div', class_='search-result-list')
    # 获取所有item
    div_list = table.find_all('div',class_='search-result-list-item')
    for div in div_list:
        # 获取每行信息
        p_list = div.find_all('p')
        img_list = div.find_all('img',class_ ='img')
        # 用于保存每行结果的字典
        item = []
        if p_list[1].text != '暂无':
            item.append(p_list [0].text)
            price_list = p_list[1].text.split('-')
            item.append(price_list[0])
            item.append(price_list[1].replace('万',''))
            item.append(img_list[0].get('src'))
        else:
            item.append(p_list[0].text)
            item.append('暂无')
            item.append('暂无')
            item.append(img_list[0].get('src'))
        df.loc[len(df)] = item

    df.drop(0, axis=0, inplace=True)
    return df


def complaint_scrap():
    global table_head
    result = pd.DataFrame(columns=table_head)
    request_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
            # 抓取每页内容
    soup = get_content(request_url)
            # 解析每页内容，结果添加在DataFrame最后
    df = content_analysis(soup)
    result = result.append(df, ignore_index=True)
    result.to_csv('bitauto-price.csv', index=False, encoding='gbk')


def main():
    complaint_scrap()


if __name__ == "__main__":
    main()