# global import
import sys

filename = sys.argv[1]

with open("output.tex", 'r', encoding='utf-8') as output:
    data = output.read()

content = "\\documentclass{article}\n\\usepackage{amsmath}\n\n\\begin{document}\n\n" + data + "\n\\end{document}"

with open("output.tex", 'w', encoding='utf-8') as output:
    output.write(content)
