# PageRank Web Crawler

## 简介

本项目实现了一个基于PageRank算法的网页爬虫和数据分析工具。PageRank算法是一种基于马尔科夫链的算法，用于评估网页的重要性。该项目提供了两种方式来获取网页链接数据：通过爬虫从指定的起始URL开始爬取网页，或从Stanford Large Network Dataset Collection (SNAP)中提取数据集。

## 项目组成

### 主要文件

- **main.py**：项目的主程序，负责根据用户选择的方式（爬虫或SNAP数据集）来获取网页链接数据，计算PageRank值，并将结果保存到CSV文件中。

- **gui.py**：图形用户界面，使用`tkinter`库实现。用户可以通过GUI选择数据获取方式、输入参数，并查看程序运行日志和结果。

- **snap_extractor.py**：负责从SNAP数据集中提取链接信息，并创建转移矩阵。用户可以指定最大节点数和最大边数来控制数据集的规模。

- **crawler.py**：实现网页爬虫功能，从指定的起始URL开始，爬取网页并提取链接信息。

- **common_crawl_extractor.py**：预留用于从Common Crawl中提取数据的功能（当前未实现）。

### 结果文件

- **custom_pagerank_results.csv**：保存自定义实现的PageRank算法计算的结果。

- **networkx_pagerank_results.csv**：保存使用`networkx`库的PageRank算法计算的结果。

### 依赖库

- **networkx**：用于图的创建和分析。
- **numpy**：用于数值计算。
- **scipy**：用于处理稀疏矩阵。
- **requests**：用于HTTP请求，获取网页内容。
- **beautifulsoup4**：用于解析HTML文档，提取网页链接。

## PageRank算法的体现

- **转移矩阵的构建**：在`create_transition_matrix`和`create_transition_matrix_from_links`函数中，构建了一个转移矩阵，表示从一个网页转移到另一个网页的概率。

- **迭代计算PageRank值**：在`page_rank`函数中，通过迭代更新每个网页的PageRank值，模拟随机浏览者在网页之间的跳转行为。

- **阻尼系数（Damping Factor）**：用于模拟随机浏览者偶尔会跳转到任意网页的行为，确保算法的稳定性。

## 马尔科夫链的体现

- **状态转移**：转移矩阵是马尔科夫链的状态转移矩阵，表示从一个状态（网页）转移到另一个状态的概率。

- **无记忆性**：PageRank算法的迭代过程符合马尔科夫链的无记忆性特征，即下一个状态只依赖于当前状态。

## 网页排名依据

- **链接结构**：PageRank算法根据网页之间的链接结构进行排名。一个网页的PageRank值越高，表示该网页被其他网页引用的次数越多，或者被高PageRank值的网页引用。

## 环境要求

- Python 3.x
- 需要安装以下Python库：
  - `requests`
  - `beautifulsoup4`
  - `numpy`
  - `scipy`
  - `networkx`

可以使用以下命令安装所需库：

```bash
pip install requests beautifulsoup4 numpy scipy networkx
```

## 运行方法

1. 确保已安装所需的Python库。
2. 在终端中导航到项目目录。
3. 运行以下命令启动图形界面：

```bash
python gui.py
```

通过图形界面，用户可以选择数据获取方式、输入参数，并查看程序运行日志和结果。程序将输出每个网页的PageRank值及其对应的URL，并将结果保存到CSV文件中。

## 注意
选取节点数和边数时候，如果选取的数目过大，可能会导致内存不足，推荐选取5000、200000
