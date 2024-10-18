import sys
import numpy as np
import csv
import networkx as nx
from crawler import crawl_web, create_transition_matrix
from snap_extractor import fetch_links_from_snap, create_transition_matrix_from_links

def page_rank(transition_matrix, num_iterations=1000, damping_factor=0.85, tolerance=1e-9):
    num_pages = transition_matrix.shape[0]
    rank = np.ones(num_pages) / num_pages
    dangling_weights = rank
    is_dangling = np.where(transition_matrix.sum(axis=1) == 0)[0]

    for iteration in range(num_iterations):
        rank_last = rank
        rank = damping_factor * (transition_matrix.T @ rank + sum(rank[is_dangling]) * dangling_weights) + (1 - damping_factor) / num_pages
        
        if np.linalg.norm(rank - rank_last, ord=1) < tolerance:
            print(f"PageRank在第{iteration+1}次迭代时收敛")
            break
        
        if iteration % 100 == 0 or iteration == num_iterations - 1:
            print(f"迭代 {iteration}: {rank}")
    
    print("PageRank计算完成。")
    return rank

def networkx_page_rank(links_dict, damping_factor=0.85):
    print("正在使用networkx计算PageRank值...")
    G = nx.DiGraph(links_dict)
    print(f"图中节点数: {G.number_of_nodes()}, 边数: {G.number_of_edges()}")
    ranks = nx.pagerank(G, alpha=damping_factor)
    print("networkx PageRank计算完成。")
    return ranks

def save_to_csv(ranks, index_to_url, filename="pagerank_results.csv"):
    rank_data = [(i, rank, index_to_url[i]) for i, rank in enumerate(ranks)]
    rank_data.sort(key=lambda x: x[1], reverse=True)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "PageRank", "Name"])
        for data in rank_data:
            writer.writerow(data)
    print(f"PageRank结果已保存到 {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供方法选择参数（1或2）")
        sys.exit(1)

    choice = sys.argv[1]

    if choice == '1':
        start_urls = [
            "https://www.sina.com.cn"
        ]
        all_links, num_pages, index_to_url, visited = crawl_web(start_urls, max_depth=2, max_pages=50)
        transition_matrix = create_transition_matrix(all_links, num_pages)
        print(f"转移矩阵规模: {transition_matrix.shape}")
        # print("转移矩阵示例（前5行）：")
        # print(transition_matrix[:5, :5].toarray())
        links_dict = {index_to_url[i]: [index_to_url[j] for j in range(num_pages) if transition_matrix[i, j] > 0] for i in range(num_pages)}
    elif choice == '2':
        if len(sys.argv) != 5:
            print("请提供SNAP数据集文件路径、最大节点数和最大边数")
            sys.exit(1)
        file_path = sys.argv[2]
        max_nodes = int(sys.argv[3])
        max_edges = int(sys.argv[4])
        links_dict = fetch_links_from_snap(file_path, max_nodes, max_edges)
        transition_matrix, url_to_index = create_transition_matrix_from_links(links_dict)
        index_to_url = {v: k for k, v in url_to_index.items()}
        print(f"转移矩阵规模: {transition_matrix.shape}")
        print("转移矩阵示例（前5行）：")
        print(transition_matrix[:5, :5].toarray())
    else:
        print("无效的选项。")
        sys.exit(1)

    custom_ranks = page_rank(transition_matrix)
    save_to_csv(custom_ranks, index_to_url, filename="custom_pagerank_results.csv")

    nx_ranks_dict = networkx_page_rank(links_dict)
    nx_ranks = [nx_ranks_dict[index_to_url[i]] for i in range(len(index_to_url))]
    save_to_csv(nx_ranks, index_to_url, filename="networkx_pagerank_results.csv")
