# 🧾 Ledgr

> A small AI-powered worker that understands invoice requests, processes local invoice files, and verifies its actions.

## 🎬 Demo

Watch Ledgr in action:

[▶ Watch Demo Video](https://www.youtube.com/watch?v=GyyrYFa-SAo)

## ✨ What it does

* Understands natural-language requests using Groq
* Finds invoices from local files
* Extracts invoice details
* Records invoices in a CSV ledger
* Detects duplicates and verifies results
* Shows execution steps and asks for approval

## ⚙️ Tech Stack

`Python` · `Streamlit` · `Groq API` · `CSV`

## 🚀 Run locally

```bash
git clone YOUR_REPOSITORY_URL
cd invoice-agent

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Start the app:

```bash
streamlit run app.py
```

## 🧠 How it works

```text
User Request
     ↓
AI Planner
     ↓
Human Approval
     ↓
Invoice Tools
     ↓
CSV Ledger
     ↓
Verification
```

## 📁 Project Structure

```text
invoice-agent/
├── app.py
├── planner.py
├── agent.py
├── tools.py
├── data/
│   ├── invoices/
│   └── ledger.csv
├── requirements.txt
└── README.md
```

## ⚠️ Current Scope

This is a prototype using local sample invoices and a CSV ledger. It supports a limited invoice-processing workflow; it is not a general-purpose autonomous agent.

## 🔮 Future Improvements

* Automatic retries
* More document formats
* Persistent memory
* Better validation and error recovery

---

<p align="center">Built as an exploration of AI agents, tool use, and reliable task execution.</p>
