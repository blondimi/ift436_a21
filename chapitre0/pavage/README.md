# Pavage

Afin de convertir un pavage en PDF:

1. Convertir la grille en LaTeX: `python3 exporter.py > pavage.tex`
2. Compiler: par ex.             `pdflatex pavage.tex`
3. Ouvrir `pavage.pdf`

_La compilation requiert le package TikZ pour LaTeX._