import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import threading
import csv

def run_program(method):
    # 清空日志
    log_text.delete(1.0, tk.END)
    
    # 选择方法
    if method == 1:
        command = "python main.py 1"
    elif method == 2:
        file_path = filedialog.askopenfilename(title="选择SNAP数据集文件", filetypes=[("Text files", "*.txt")])
        if not file_path:
            messagebox.showerror("错误", "请选择SNAP数据集文件")
            return
        max_nodes = simpledialog.askinteger("最大节点数", "请输入要读取的最大节点数（留空使用默认值）", initialvalue=100000)
        max_edges = simpledialog.askinteger("最大边数", "请输入要读取的最大边数（留空使用默认值）", initialvalue=2552519)
        command = f"python main.py 2 \"{file_path}\" {max_nodes} {max_edges}"
    else:
        messagebox.showerror("错误", "请选择一种方法")
        return

    # 使用线程运行程序
    thread = threading.Thread(target=execute_command, args=(command,))
    thread.start()

def execute_command(command):
    # 运行程序并捕获输出
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        log_text.insert(tk.END, line)
        log_text.see(tk.END)
        root.update_idletasks()

    process.stdout.close()
    process.wait()

    if process.returncode != 0:
        messagebox.showerror("错误", "程序运行出错，请查看日志")
    else:
        messagebox.showinfo("完成", "程序运行完成")
        # 自动展示CSV文件内容
        display_csv("custom_pagerank_results.csv", custom_tree)
        display_csv("networkx_pagerank_results.csv", networkx_tree)

def display_csv(file_path, tree):
    # 清空Treeview
    for item in tree.get_children():
        tree.delete(item)

    # 读取CSV文件的前100行
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        tree["columns"] = headers
        for col in headers:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for i, row in enumerate(reader):
            if i >= 100:  # 只显示前100行
                break
            tree.insert("", "end", values=row)

# 创建主窗口
root = tk.Tk()
root.title("基于马尔可夫链的PageRank算法实现")

# 方法选择
method_frame = ttk.LabelFrame(root, text="选择方法")
method_frame.pack(padx=10, pady=10, fill="x")

method_var = tk.IntVar()
method1_radio = ttk.Radiobutton(method_frame, text="方法1：使用爬虫", variable=method_var, value=1)
method1_radio.pack(anchor="w", padx=5, pady=5)
method1_radio.bind("<Enter>", lambda e: log_text.insert(tk.END, "方法1：使用爬虫从指定的起始URL开始，爬取网页并计算PageRank值。\n"))

method2_radio = ttk.Radiobutton(method_frame, text="方法2：从SNAP数据集中提取数据", variable=method_var, value=2)
method2_radio.pack(anchor="w", padx=5, pady=5)
method2_radio.bind("<Enter>", lambda e: log_text.insert(tk.END, "方法2：从SNAP数据集中提取链接信息并计算PageRank值。\n"))

# 日志查看
log_frame = ttk.LabelFrame(root, text="日志")
log_frame.pack(padx=10, pady=10, fill="both", expand=True)

log_text = tk.Text(log_frame, wrap=tk.WORD, height=10)
log_text.pack(padx=5, pady=5, fill="both", expand=True)

# 结果查看
result_frame = ttk.LabelFrame(root, text="结果查看")
result_frame.pack(padx=10, pady=10, fill="both", expand=True)

# 自定义PageRank结果
custom_frame = ttk.LabelFrame(result_frame, text="自定义PageRank结果")
custom_frame.pack(padx=5, pady=5, fill="both", expand=True)

custom_tree = ttk.Treeview(custom_frame, show="headings")
custom_tree.pack(padx=5, pady=5, fill="both", expand=True)

# networkx PageRank结果
networkx_frame = ttk.LabelFrame(result_frame, text="networkx PageRank结果")
networkx_frame.pack(padx=5, pady=5, fill="both", expand=True)

networkx_tree = ttk.Treeview(networkx_frame, show="headings")
networkx_tree.pack(padx=5, pady=5, fill="both", expand=True)

# 按钮
button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10, fill="x")

start_button = ttk.Button(button_frame, text="开始", command=lambda: run_program(method_var.get()))
start_button.pack(side="left", padx=5, pady=5)

# 运行主循环
root.mainloop()
