import re
import glob
import os

# Encuentra todos los archivos .tex
archivos = glob.glob("*.tex")

# Ordenar por fecha de creación (o change time en Unix)
#archivos.sort(key=os.path.getctime)
archivos.sort()

# Expresión regular para extraer preguntas dentro de \begin{questions}...\end{questions}
patron = re.compile(
    r'\\begin\{questions\}(.*?)\\end\{questions\}',
    re.DOTALL | re.IGNORECASE
)

preguntas = []

for archivo in archivos:
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
        bloques = patron.findall(contenido)
        for bloque in bloques:
            # Elimina \vspace{...} o \vspace*{...}
            bloque = re.sub(r'\\vspace\*?\s*\{.*?\}', '', bloque)
            # Elimina \newpage (con o sin espacios)
            bloque = re.sub(r'\\newpage\s*', '', bloque)
            preguntas.append(f"% Preguntas extraídas de: {archivo}\n{bloque.strip()}")

# Encabezado completo LaTeX
encabezado = r"""
\documentclass[spanish, 11pt]{exam}

\usepackage{array,epsfig}
\usepackage{amsmath, textcomp}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{amsxtra}
\usepackage{amsthm}
\usepackage{mathrsfs}
\usepackage{color}
\usepackage{multicol, xparse}
\usepackage{verbatim}
\usepackage{booktabs}

\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{eurosym}

\usepackage{graphicx}
\graphicspath{{../img/}}
\usepackage{pgf}

\usepackage{pgf,tikz,pgfplots}
\pgfplotsset{compat=1.15}
\usepackage{mathrsfs}
\usetikzlibrary{arrows}

%\printanswers
\nopointsinmargin
\pointformat{}

\let\multicolmulticols\multicols
\let\endmulticolmulticols\endmulticols
\RenewDocumentEnvironment{multicols}{mO{}}
 {%
  \ifnum#1=1
    #2%
  \else
    \multicolmulticols{#1}[#2]
  \fi
 }
 {%
  \ifnum#1=1
  \else
    \endmulticolmulticols
  \fi
 }

\renewcommand{\solutiontitle}{\noindent\textbf{Sol:}\enspace}
\newcommand{\samedir}{\mathbin{\!/\mkern-5mu/\!}}

\newcommand{\class}{1º Bachillerato}
\newcommand{\examdate}{\today}
\newcommand{\tipo}{A}
\newcommand{\timelimit}{50 minutos}

\pagestyle{head}
\firstpageheader{Dep. Matemáticas}{Preparación de prueba global}{IES Goya}
\runningheader{IES Goya}{Preparación de prueba global}{Página \thepage\ de \numpages}
\runningheadrule
"""

# Escribir todas las preguntas en un nuevo archivo LaTeX
with open("todas_las_preguntas.tex", 'w', encoding='utf-8') as f:
    f.write(encabezado + "\n\\begin{document}\n\\begin{questions}\n")
    for bloque in preguntas:
        f.write(bloque + "\n\n")
    f.write("\\end{questions}\n\\end{document}\n")
