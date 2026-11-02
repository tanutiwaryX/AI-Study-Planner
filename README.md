# MindSpace AI — AI Study Planner

A modern purple-themed Streamlit application for analyzing study notes, planning study sessions, tracking history, viewing charts, and exporting PDF reports.

## Features
- Modern purple SaaS-style interface with five pages
- TextBlob sentiment classification (Positive, Neutral, Negative)
- NLTK tokenization, stop-word removal, and lemmatization
- Extractive summary by default
- Optional Hugging Face abstractive summarization
- SQLite local analysis history
- Pandas and Plotly dashboard charts
- PDF report generation with ReportLab
- CSV export of analysis history

## Technology
Python 3.10+, Streamlit, TextBlob, NLTK, Hugging Face Transformers (optional), PyTorch (optional), SQLite, Pandas, Plotly, ReportLab, VS Code.

## Setup on Windows
Open this folder in VS Code and run:

```powershell
py -3.12 -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501 if the browser does not open automatically.

## Optional summarization model
The default summary does not need PyTorch. To use Hugging Face abstractive summarization, uncomment `transformers` and `torch` in `requirements.txt`, install them with a supported Python/PyTorch combination, and select the option on Analyze Notes. The first run downloads the model and may require substantial disk space, RAM, and internet bandwidth.

## Database
The `study_planner.db` SQLite file is created automatically in the project folder and stores analysis history locally.
