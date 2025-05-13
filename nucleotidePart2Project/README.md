# 🔬 Nucleotide Pattern CLI Search Tool

A classic Python command-line application that fetches a nucleotide sequence from the **NCBI database** and allows regex-based search across it. It caches both the sequence and match results using **Memcached** to optimize repeated queries.

---

## 🧩 Features

- 🧬 Fetch nucleotide sequences from NCBI via `efetch`
- 🔍 Search the sequence using any valid Python regex pattern
- ⚡ Optional Memcached caching for sequences and pattern matches
- 🖥️ Pure Python script — no web server or frontend required
- 📦 Easily extensible for output, filtering, or ID list scanning

---

### 1. Clone the Repository

```bash
git clone https://github.com/AvenashKumar/nucleotide-project.git
cd nucleotide-project/nucleotidePart2Project
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

### 5. Usage

```bash
python main.py "ATG[CT]" (By default this will use id=224589800)
python nucleotide_search.py "AATTGC" --id 30271926
python nucleotide_search.py "GG[AT]{2}" --no-cache
```

### 6. Libraries

| Library          | Purpose                                                                                  |
| ---------------- | ---------------------------------------------------------------------------------------- |
| **`requests`**   | Makes HTTP requests to NCBI's efetch API to retrieve nucleotide sequences                |
| **`pymemcache`** | Lightweight Python client for Memcached, used to cache sequences and regex match results |
