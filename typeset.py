"""Basic Typeset for the LaTeX formatting
"""
# global import
import sys

filename = sys.argv[1]

with open(filename, 'r', encoding='utf-8') as output:
    data = output.read()

content = "\\documentclass{article}\n\\usepackage{amsmath}\n\n\\begin{document}\n\n" + data + "\n\\end{document}"

with open(filename, 'w', encoding='utf-8') as output:
    output.write(content)
