# AI Prompt Comparison Homework

Submission for Pham Ha Linh, student ID 26090224, SIS VNU.

## Submission

`Pham-Ha-Linh-26090224.pdf` contains the four-page report followed by the full
raw responses from Qwen3.8-27B and GPT-OSS-120B.

## Reproduction

`run_groq.py` runs the nine prompts from `thu-nghiem.json` with the API key in
the local `.env` file. `build_report.py` generates the main report and
`export_appendix.py` generates the comparison appendix. Compile `bao-cao.tex`
with XeLaTeX and BibTeX when rebuilding the report.

The raw response logs are included as `groq-qwen.json` and `groq-results.json`.
