#!/bin/sh
# Builds main.pdf: pdflatex, biber, pdflatex, pdflatex
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode main.tex >/dev/null && biber main >/dev/null && pdflatex -interaction=nonstopmode main.tex >/dev/null && pdflatex -interaction=nonstopmode main.tex >/dev/null
echo "build exit: $?"
