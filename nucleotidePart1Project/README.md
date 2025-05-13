# 🔬 Nucleotide Pattern Search (Django App)

This Django-based web app allows users to fetch nucleotide sequences from the **NCBI database** and run **regular expression-based searches** on them. It supports both form-based and query parameter-based searches.

Users can search using regex patterns like `(AATCGA|GGCAT)` to identify all matching regions in the sequence.

---

## 📦 Features

- 🔁 Fetches nucleotide sequence from NCBI using `efetch`
- 🔍 Supports regex-based search (e.g., `(AATCGA|GGCAT)`)
- 🧠 Uses Memcached for caching fetched sequences
- 🌐 Accepts input from both **form submissions** and **URL query parameters**
- 🧪 Highlights (optionally) all matched regions in the sequence

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AvenashKumar/nucleotide-project.git
cd nucleotide-project
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install Dependencies

```pip
pip install -r requirements.txt
```

### 4. Run Memcached Locally (macOS example)

```bash
brew install memcached
brew services start memcached
```

### 5. Start the Django Server

```bash
python manage.py runserver
```

### 6. Access the App

```bash
http://127.0.0.1:8000/?pattern=(AATCGA|GGCAT)
```