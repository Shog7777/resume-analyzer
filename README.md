# 🎯 Resume Analyzer — ATS Matcher

An AI-powered resume analyzer that compares your resume with a job description and gives you a detailed ATS match score.

## Features

- 📄 Upload PDF or DOCX resume (or paste text)
- 💼 Paste any job description
- 🤖 AI-powered analysis using Claude
- 📊 Detailed scores: Overall, Skills, Experience, Keywords
- ✅ Matched & ❌ Missing keywords
- 💡 Improvement suggestions
- 🎨 Clean dark UI

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Shog7777/resume-analyzer.git
cd resume-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```
Get your API key from [console.anthropic.com](https://console.anthropic.com)

### 4. Run the app
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

1. Upload your resume (PDF/DOCX) or paste the text
2. Paste the job description
3. Click **Analyze Match**
4. Review your ATS score and improvement suggestions

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Anthropic Claude (claude-sonnet-4-6)
- **PDF parsing**: pdfplumber
- **DOCX parsing**: python-docx

## License

MIT
