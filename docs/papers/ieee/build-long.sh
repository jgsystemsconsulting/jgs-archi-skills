#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
JOB=soam-ieee-long
pdflatex -interaction=nonstopmode "$JOB"
bibtex "$JOB"
pdflatex -interaction=nonstopmode "$JOB"
pdflatex -interaction=nonstopmode "$JOB"
echo "PDF: $ROOT/${JOB}.pdf"
