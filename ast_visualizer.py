"""
AST Generator and Visualizer — Compiler Design Mini Project
Run: python ast_visualizer.py
Example input: result = a + b * 2
"""
import ast
import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt
import networkx as nx


def ast_to_graph(node, graph=None, parent=None, edge_label=""):
    """Recursively convert Python AST nodes into a directed graph."""
    if graph is None:
        graph = nx.DiGraph()

    node_id = id(node)
    label = type(node).__name__

    if isinstance(node, ast.Name):
        label += f"\\n({node.id})"
    elif isinstance(node, ast.Constant):
        label += f"\\n({node.value})"
    elif isinstance(node, (ast.operator, ast.unaryop, ast.cmpop)):
        label = type(node).__name__

    graph.add_node(node_id, label=label)
    if parent is not None:
        graph.add_edge(parent, node_id, label=edge_label)

    for field, value in ast.iter_fields(node):
        if isinstance(value, ast.AST):
            ast_to_graph(value, graph, node_id, field)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, ast.AST):
                    ast_to_graph(item, graph, node_id, f"{field}[{index}]")
    return graph


def draw_ast(source_code):
    """Parse entered code and display its AST."""
    try:
        tree = ast.parse(source_code, mode="exec")
    except SyntaxError as error:
        messagebox.showerror(
            "Syntax Error",
            f"Could not parse the code.\\nLine {error.lineno}: {error.msg}"
        )
        return

    graph = ast_to_graph(tree)
    labels = nx.get_node_attributes(graph, "label")

    # Graphviz gives a hierarchical tree layout; use a fallback if unavailable.
    try:
        from networkx.drawing.nx_agraph import graphviz_layout
        positions = graphviz_layout(graph, prog="dot")
    except Exception:
        positions = nx.spring_layout(graph, seed=7)

    plt.figure(figsize=(12, 7))
    nx.draw_networkx(
        graph, positions, labels=labels, with_labels=True,
        node_size=2600, node_color="#d9ecff", edge_color="#526783",
        font_size=8, arrows=False, linewidths=1.2
    )
    nx.draw_networkx_edge_labels(
        graph, positions, edge_labels=nx.get_edge_attributes(graph, "label"),
        font_size=7
    )
    plt.title("Abstract Syntax Tree (AST)", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    root = tk.Tk()
    root.title("AST Generator and Visualizer")
    root.geometry("760x520")
    root.configure(bg="#101b33")

    tk.Label(
        root, text="AST GENERATOR & VISUALIZER",
        font=("Times New Roman", 20, "bold"), fg="white", bg="#101b33"
    ).pack(pady=(18, 8))

    tk.Label(
        root,
        text="Enter Python code below and generate its Abstract Syntax Tree.",
        font=("Times New Roman", 12), fg="#b9c9e3", bg="#101b33"
    ).pack(pady=(0, 10))

    editor = scrolledtext.ScrolledText(
        root, height=8, width=75, font=("Consolas", 12),
        bg="#f5f8ff", fg="#17243c", insertbackground="#17243c"
    )
    editor.pack(padx=20, pady=8)
    editor.insert("1.0", "result = a + b * 2")

    tk.Button(
        root, text="Generate AST",
        command=lambda: draw_ast(editor.get("1.0", tk.END).strip()),
        font=("Times New Roman", 13, "bold"), bg="#39cbd4", fg="#101b33",
        activebackground="#79e2e7", padx=18, pady=8, cursor="hand2"
    ).pack(pady=14)

    tk.Label(
        root,
        text="Example: total = price + tax  |  Supports valid Python syntax",
        font=("Times New Roman", 10), fg="#b9c9e3", bg="#101b33"
    ).pack(pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
