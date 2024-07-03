import string
import os
import matplotlib.pyplot as plt
import networkx as nx
import random
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import sys

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