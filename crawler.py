import requests
from bs4 import BeautifulSoup
from collections import deque
import numpy as np
import random

def fetch_links(url, max_links_per_page=100):
    """
    从给定的URL中提取所有链接
    :param url: 网页的URL
    :param max_links_per_page: 每个页面最多提取的链接数
    :return: 链接列表
    """
    try:
        print(f"正在从 {url} 获取链接...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        # 过滤掉无效链接
        valid_links = [link for link in links if link.startswith('http')]
        # 随机选择一部分链接
        if len(valid_links) > max_links_per_page:
            valid_links = random.sample(valid_links, max_links_per_page)
        print(f"找到 {len(valid_links)} 个有效链接。")
        return valid_links
    except Exception as e:
        print(f"获取 {url} 时出错: {e}")
        return []

def crawl_web(start_urls, max_depth=2, max_pages=50, max_links_per_page=100):
    """
    爬取网页，限制爬虫深度和总页面数量
    :param start_urls: 起始URL列表
    :param max_depth: 最大爬虫深度
    :param max_pages: 最大页面数量
    :param max_links_per_page: 每个页面最多提取的链接数
    :return: 链接列表，页面总数，页面索引到URL的映射，访问过的URL集合
    """
    visited = set()
    queue = deque([(url, 0) for url in start_urls])
    all_links = []
    url_to_index = {url: idx for idx, url in enumerate(start_urls)}
    index_to_url = {idx: url for idx, url in enumerate(start_urls)}
    current_index = len(start_urls)
    total_visited = 0

    while queue and total_visited < max_pages:
        url, depth = queue.popleft()
        if url not in visited and depth <= max_depth:
            print(f"正在访问: {url}，深度 {depth}")
            visited.add(url)
            total_visited += 1
            links = fetch_links(url, max_links_per_page)
            for link in links:
                if link not in visited and link not in url_to_index:
                    if len(visited) >= max_pages:
                        break
                    url_to_index[link] = current_index
                    index_to_url[current_index] = link
                    current_index += 1
                    queue.append((link, depth + 1))
                    all_links.append((url_to_index[url], url_to_index[link]))

    print(f"总共访问了 {total_visited} 个页面。")
    return all_links, len(url_to_index), index_to_url, visited

def create_transition_matrix(links, num_pages):
    """
    创建转移矩阵
    :param links: 网页链接的列表，每个元素是一个元组 (from_page, to_page)
    :param num_pages: 网页的总数
    :return: 转移矩阵
    """
    transition_matrix = np.zeros((num_pages, num_pages))
    
    for from_page, to_page in links:
        transition_matrix[from_page][to_page] += 1
    
    for i in range(num_pages):
        row_sum = np.sum(transition_matrix[i])
        if row_sum > 0:
            transition_matrix[i] /= row_sum
        else:
            transition_matrix[i] = np.ones(num_pages) / num_pages
    
    print("转移矩阵已创建。")
    return transition_matrix
