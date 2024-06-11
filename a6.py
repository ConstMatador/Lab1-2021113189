import string
import os
import matplotlib.pyplot as plt
import networkx as nx
import random
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import sys


def process_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    text = ''.join(filter(lambda x: x.isalpha() or x.isspace(), text))
    text = text.lower()
    words = text.split()
    return words


# 构建map
def build_tuple_map(words):
    tuple_map = {}
    for i in range(len(words) - 1):
        x, y = words[i], words[i + 1]
        if x != y:
            if (x, y) not in tuple_map:
                tuple_map[(x, y)] = 1
            else:
                tuple_map[(x, y)] += 1
        elif i < len(words) - 2 and words[i] == words[i + 1]:
            if (x, y) not in tuple_map:
                tuple_map[(x, y)] = 1
            else:
                tuple_map[(x, y)] += 1
    return tuple_map


# 将map写入到文件存储
def write_tuple_map_to_file(tuple_map, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for key, value in tuple_map.items():
            x, y = key
            if x != y:
                file.write(f"{x} {y} {value}\n")


# 绘制有向图的函数
def draw_graph(file_path, canvas):
    G = nx.DiGraph()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    source, target, weight = parts
                    G.add_edge(source, target, weight=float(weight))
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

    # pos = nx.spring_layout(G, k=0.1, iterations=100)
    pos = nx.circular_layout(G)
    # pos = nx.shell_layout(G)
    # pos = nx.kamada_kawai_layout(G)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, arrows=True, node_color='skyblue', node_size=1500,
            edge_color='gray', font_size=12, font_weight='bold', arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', label_pos=0.3)
    plt.title("")
    plt.savefig("graph.png")
    plt.close()
    canvas.delete("all")
    img = tk.PhotoImage(file="graph.png")
    canvas.image = img
    canvas.create_image(0, 0, anchor=tk.NW, image=img)


# 读取文件，构建有向图
def read_graph_from_file(file_path):
    G = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                source, target, weight = parts
                weight = float(weight)
                if source not in G:
                    G[source] = []
                G[source].append((target, weight))
    return G


# 查找两个节点之间的直接中继节点
def search_direct_intermediate_nodes(graph, start_node, end_node):
    intermediate_nodes = set()
    all_nodes = set(graph.keys()) | set(node for edges in graph.values() for node, _ in edges)
    if start_node not in all_nodes or end_node not in all_nodes:
        return "没有" + start_node + "或" + end_node
    if any(neighbor == end_node for neighbor, _ in graph.get(start_node, [])):
        return start_node + "和" + end_node + "之间没有桥接词"
    for neighbor, _ in graph.get(start_node, []):
        if any(next_hop == end_node for next_hop, _ in graph.get(neighbor, [])):    
            intermediate_nodes.add(neighbor)
    if not intermediate_nodes:
        return start_node + "和" + end_node + "之间没有桥接词"
    return start_node + "和" + end_node + "之间的桥接词是" + ", ".join(intermediate_nodes)


# 两个节点之间的直接中继节点
def insert_direct_intermediate_nodes(graph, start_node, end_node):
    # print(start_node + " " + end_node)
    intermediate_nodes = set()
    all_nodes = set(graph.keys()) | set(node for edges in graph.values() for node, _ in edges)
    if start_node not in all_nodes or end_node not in all_nodes:
        return None
    if any(neighbor == end_node for neighbor, _ in graph.get(start_node, [])):
        return set()
    for neighbor, _ in graph.get(start_node, []):
        if any(next_hop == end_node for next_hop, _ in graph.get(neighbor, [])):
            intermediate_nodes.add(neighbor)
    print(intermediate_nodes)
    return intermediate_nodes


# 处理英文语句，插入直接中继节点
def insert_bridge_words(graph, sentence):
    words = sentence.split()
    new_sentence = []
    for i in range(len(words) - 1):
        new_sentence.append(words[i])
        direct_intermediate_nodes = insert_direct_intermediate_nodes(graph, words[i], words[i + 1])
        if direct_intermediate_nodes:
            intermediate_node = random.choice(list(direct_intermediate_nodes))
            new_sentence.append(intermediate_node)
    new_sentence.append(words[-1])
    for i in range(len(new_sentence)):
        if i < len(words):
            if words[i].istitle():
                new_sentence[i] = new_sentence[i].capitalize()
    return ' '.join(new_sentence)


# 从文件中读取图并构建有向图的函数
def get_graph(file_path):
    G = nx.DiGraph()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    source, target, weight = parts
                    G.add_edge(source, target, weight=float(weight))
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")
    return G


# 查找单个节点到所有其他节点的最短路径
def find_all_shortest_paths(G, source):
    try:
        paths = nx.single_source_dijkstra_path(G, source, weight='weight')
        return paths
    except nx.NodeNotFound as e:
        print(e)
        return None


# 查找两个节点之间最短路径的函数
def find_shortest_path(G, source, target):
    try:
        path = nx.shortest_path(G, source=source, target=target, weight='weight')
        return path
    except nx.NetworkXNoPath:
        print(f"在 {source} 和 {target} 之间没有路径")
        return None
    except nx.NodeNotFound as e:
        print(e)
        return None


# 绘制有向图并突出显示最短路径的函数
def draw_shortest_path(G, source, target, canvas, shortest_path=None):
    # pos = nx.spring_layout(G, k=0.1, iterations=100)
    pos = nx.circular_layout(G)
    # pos = nx.shell_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, arrows=True, node_color='skyblue', node_size=1500,
            edge_color='gray', font_size=12, font_weight='bold', arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', label_pos=0.3)
    if shortest_path:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)
    plt.title("")
    plt.savefig("shortest_path.png")
    plt.close()
    canvas.delete("all")
    img = tk.PhotoImage(file="shortest_path.png")
    canvas.image = img
    canvas.create_image(0, 0, anchor=tk.NW, image=img)


# 绘制有向图并突出显示路径的函数
def draw_graph_with_path(G, path, canvas):
    # pos = nx.spring_layout(G, k=0.1, iterations=100)
    pos = nx.circular_layout(G)
    # pos = nx.shell_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, arrows=True, node_color='skyblue', node_size=1500,
            edge_color='gray', font_size=12, font_weight='bold', arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_edges(G, pos, edgelist=path, edge_color='red', width=2)  # 绘制路径上的边
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', label_pos=0.3)
    plt.title("")
    plt.savefig("path_graph.png")
    plt.close()
    canvas.delete("all")
    img = tk.PhotoImage(file="path_graph.png")
    canvas.image = img
    canvas.create_image(0, 0, anchor=tk.NW, image=img)


# 执行随机遍历并记录边的函数
def random_traversal_with_edges(G):
    if len(G) == 0:
        print("图中没有节点。")
        return [], []
    current_node = random.choice(list(G.nodes()))
    visited_nodes = set()
    visited_edges = []
    print("随机遍历开始，起点节点:", current_node)
    while True:
        if current_node in visited_nodes:
            print("遍历停止：回到已访问的节点", current_node)
            break
        visited_nodes.add(current_node)
        out_edges = list(G.out_edges(current_node))
        if not out_edges:
            print("遍历停止：节点", current_node, "不存在出边")
            break
        next_edge = random.choice(out_edges)
        visited_edges.append(next_edge)
        next_node = next_edge[1]
        print("遍历到节点:", next_node)
        current_node = next_node
        continue_walk = messagebox.askyesno("继续游走", "是否继续游走？")
        if not continue_walk:
            print("用户选择停止遍历。")
            break
    print(visited_nodes)
    print(visited_edges)
    return visited_nodes, visited_edges
    

# 将访问的节点写入文件的函数
def write_visited_nodes_to_file(visited_nodes):
    file_path = "./path/path.txt"
    with open(file_path, 'w') as file:
        for node in visited_nodes:
            file.write(node + ' ')
    print(f"已将遍历的节点写入到文件 {file_path}")


class RedirectText(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, string)
        self.widget.configure(state='disabled')
        self.widget.see(tk.END)

    def flush(self):
        pass


class CommandLineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图处理工具")
        self.geometry("1300x700")

        self.output_text = tk.Text(self, wrap=tk.WORD, state='disabled')
        self.output_text.grid(row=0, column=0, sticky="nsew")

        sys.stdout = RedirectText(self.output_text)
        sys.stderr = RedirectText(self.output_text)

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.btn_choose_file = tk.Button(self.button_frame, text="选择文本文件", command=self.choose_file)
        self.btn_choose_file.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_query_bridge_words = tk.Button(self.button_frame, text="查询桥接词", command=self.query_bridge_words)
        self.btn_query_bridge_words.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_generate_new_text = tk.Button(self.button_frame, text="生成新文本", command=self.generate_new_text)
        self.btn_generate_new_text.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_compute_shortest_path = tk.Button(self.button_frame, text="计算最短路径", command=self.compute_shortest_path)
        self.btn_compute_shortest_path.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_random_walk = tk.Button(self.button_frame, text="随机游走", command=self.random_walk)
        self.btn_random_walk.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_quit = tk.Button(self.button_frame, text="退出程序", command=self.quit)
        self.btn_quit.pack(side=tk.RIGHT, padx=5, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=100)


    def update_output(self, text):
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.configure(state='disabled')
        self.output_text.see(tk.END)


    def choose_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                words = process_text(file_path)
                tuple_map = build_tuple_map(words)
                write_tuple_map_to_file(tuple_map, './graph/graph.txt')
                draw_graph('./graph/graph.txt', self.canvas)
                self.update_output("文件已成功处理并生成有向图。")
            except Exception as e:
                self.update_output(f"处理文件时发生错误: {e}")


    def query_bridge_words(self):
        if not os.path.exists('./graph/graph.txt'):
            self.update_output("请先生成有向图 (选择功能 1)。")
            return
        start_node = simpledialog.askstring("输入", "请输入起始节点:")
        end_node = simpledialog.askstring("输入", "请输入目标节点:")
        if start_node and end_node:
            graph = read_graph_from_file('./graph/graph.txt')
            result = search_direct_intermediate_nodes(graph, start_node, end_node)
            self.update_output(result)


    def generate_new_text(self):
        if not os.path.exists('./graph/graph.txt'):
            self.update_output("请先生成有向图 (选择功能 1)。")
            return
        input_sentence = simpledialog.askstring("输入", "请输入英文语句:")
        if input_sentence:
            graph = read_graph_from_file('./graph/graph.txt')
            processed_sentence = insert_bridge_words(graph, input_sentence)
            self.update_output("处理后的英文语句: " + processed_sentence)


    def compute_shortest_path(self):
        if not os.path.exists('./graph/graph.txt'):
            self.update_output("请先生成有向图 (选择功能 1)。")
            return
        source_node = simpledialog.askstring("输入", "请输入源节点:")
        target_node = simpledialog.askstring("输入", "请输入目标节点 (若无则留空):")
        if source_node:
            graph = get_graph('./graph/graph.txt')
            if source_node not in graph.nodes:
                self.update_output(f"{source_node} 不存在于图中。")
            else:
                if target_node and target_node not in graph.nodes:
                    self.update_output(f"{target_node} 不存在于图中。")
                else:
                    if not target_node:
                        target_node = random.choice(list(graph.nodes))
                    shortest_path = find_shortest_path(graph, source_node, target_node)
                    if shortest_path is None:
                        self.update_output("在 " + source_node + " 和 " + target_node + " 之间没有路径")
                    else:
                        draw_shortest_path(graph, source_node, target_node, self.canvas, shortest_path)


    def random_walk(self):
        if not os.path.exists('./graph/graph.txt'):
            self.update_output("请先生成有向图 (选择功能 1)。")
            return
        graph = get_graph('./graph/graph.txt')
        visited_nodes, visited_edges = random_traversal_with_edges(graph)
        write_visited_nodes_to_file(visited_nodes)
        draw_graph_with_path(graph, visited_edges, self.canvas)


if __name__ == "__main__":
    app = CommandLineApp()
    app.mainloop()
    os.remove("./graph/graph.txt")
    os.remove("./path/path.txt")