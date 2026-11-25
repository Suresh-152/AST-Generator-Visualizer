AST Generator and Visualizer — Compiler Design Mini Project

Files:
- ast_visualizer.py: Python program with GUI and AST visualization
- algorithm.txt: project algorithm
- requirements.txt: required Python libraries

Windows setup:
1. Install Python 3.10 or newer.
2. Open PowerShell in this folder.
3. Install libraries: py -m pip install -r requirements.txt
4. Run the app: py ast_visualizer.py

Test input:
result = a + b * 2

Expected result:
A Matplotlib window displays the AST hierarchy. Multiplication is nested beneath
addition, showing operator precedence. The assignment node connects the target
variable `result` and the expression tree.

Note:
The program uses Python's built-in ast module, so it parses Python syntax.
Graphviz is optional; if unavailable, a fallback layout is used.
