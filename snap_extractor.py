import numpy as np
import networkx as nx
from scipy.sparse import lil_matrix

def fetch_links_from_snap(file_path=None, max_nodes=None, max_edges=None):
    """
    从SNAP数据集中提取链接信息
    :param file_path: SNAP数据集文件路径
    :param max_nodes: 最大读取的节点数
    :param max_edges: 最大读取的边数
    :return: 链接字典，键为网页URL，值为该网页链接到的URL列表
    """
    if not file_path:
        file_path = 'web-Google.txt'  # 默认路径

    print(f"正在从文件 {file_path} 中读取链接信息...")
    G = nx.DiGraph()
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith('#'):
                continue
            u, v = map(int, line.split())
            if max_nodes and (u >= max_nodes or v >= max_nodes):
                continue
            G.add_edge(u, v)
            if max_edges and G.number_of_edges() >= max_edges:
                break

    print(f"图中节点数: {G.number_of_nodes()}, 边数: {G.number_of_edges()}")
    links_dict = {str(node): [str(neighbor) for neighbor in G.neighbors(node)] for node in G.nodes()}
    print(f"提取到的链接字典大小: {len(links_dict)}")
    return links_dict

def create_transition_matrix_from_links(links_dict):
    """
    根据链接字典创建转移矩阵
    :param links_dict: 链接字典，键为网页URL，值为该网页链接到的URL列表
    :return: 转移矩阵，URL到索引的映射
    """
    print("正在创建转移矩阵...")
    url_to_index = {url: idx for idx, url in enumerate(links_dict.keys())}
    num_pages = len(url_to_index)
    transition_matrix = lil_matrix((num_pages, num_pages))

    for from_url, to_urls in links_dict.items():
        from_idx = url_to_index[from_url]
        for to_url in to_urls:
            if to_url in url_to_index:
                to_idx = url_to_index[to_url]
                transition_matrix[from_idx, to_idx] += 1

    print("转移矩阵的非零元素数:", transition_matrix.nnz)
    for i in range(num_pages):
        row_sum = transition_matrix[i].sum()
        if row_sum > 0:
            transition_matrix[i] /= row_sum
        else:
            transition_matrix[i] = np.ones(num_pages) / num_pages
        if i % 1000 == 0:
            print(f"已处理 {i} 行，共 {num_pages} 行")

    print("转移矩阵创建完成。")
    return transition_matrix.tocsr(), url_to_index

if __name__ == "__main__":
    # 示例SNAP数据集文件路径
    file_path = input("请输入SNAP数据集文件的路径（留空使用默认路径）：")
    max_nodes = int(input("请输入要读取的最大节点数（留空使用默认值）：") or 100000)  # 默认读取10万节点
    max_edges = int(input("请输入要读取的最大边数（留空使用默认值）：") or 2552519)  # 默认读取一半的边数
    
    links_dict = fetch_links_from_snap(file_path, max_nodes, max_edges)
    transition_matrix, url_to_index = create_transition_matrix_from_links(links_dict)
    
    print("转移矩阵已创建。")
    print("URL到索引的映射：", url_to_index)
