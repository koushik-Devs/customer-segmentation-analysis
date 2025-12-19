@echo off
echo Cleaning auxiliary files...
del customer_segmentation_report.aux 2>nul
del customer_segmentation_report.toc 2>nul
del customer_segmentation_report.lof 2>nul
del customer_segmentation_report.lot 2>nul
del customer_segmentation_report.out 2>nul
del customer_segmentation_report.log 2>nul

echo Compiling LaTeX document (first pass)...
pdflatex -interaction=nonstopmode customer_segmentation_report.tex

echo Compiling LaTeX document (second pass for TOC)...
pdflatex -interaction=nonstopmode customer_segmentation_report.tex

echo Done! Check customer_segmentation_report.pdf
pause
