import re
import urllib.parse
import requests
import xml.etree.ElementTree as ET
from pymemcache.client import base

# -----------------------------
# Configuration
# -----------------------------
NCBI_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
CACHE_KEY_PREFIX = "nucleotide_sequence_"
CACHE_TIMEOUT = 3600  # in seconds

# -----------------------------
# Fetch from NCBI or Cache
# -----------------------------
def fetch_sequence(sequence_id, use_cache=True):
    cache_key = f"{CACHE_KEY_PREFIX}{sequence_id}"

    if use_cache:
        try:
            client = base.Client(('localhost', 11211))
            cached = client.get(cache_key)
            if cached:
                return cached.decode()
        except Exception:
            pass  # Fail silently if memcached is not running

    params = {
        "db": "nucleotide",
        "id": sequence_id,
        "rettype": "fasta",
        "retmode": "xml"
    }

    response = requests.get(NCBI_EFETCH_URL, params=params)
    response.raise_for_status()

    xml_root = ET.fromstring(response.text)
    tseq_sequence = xml_root.find('.//TSeq_sequence')
    sequence = tseq_sequence.text.strip().upper()

    if use_cache:
        try:
            client.set(cache_key, sequence.encode(), expire=CACHE_TIMEOUT)
        except Exception:
            pass

    return sequence

# -----------------------------
# Run Regex Search
# -----------------------------
def search_pattern(sequence, pattern, sequence_id, use_cache=True):
    try:
        # Use hash of sequence if no ID is provided
        sequence_key = sequence_id
        escaped_pattern = urllib.parse.quote(pattern, safe='')
        cache_key = f"pattern_matches::{sequence_key}::{escaped_pattern}"

        if use_cache:
            try:
                client = base.Client(('localhost', 11211))
                cached = client.get(cache_key)
                if cached:
                    print("Loaded matches from cache.")
                    import json
                    return json.loads(cached.decode())
            except Exception:
                pass  # Silent cache failure fallback

        regex = re.compile(pattern)
        matches = [{
            "match": m.group(),
            "start": m.start(),
            "end": m.end()
        } for m in regex.finditer(sequence)]

        if use_cache:
            try:
                import json
                client.set(cache_key, json.dumps(matches).encode(), expire=3600)
            except Exception:
                pass

        return matches

    except re.error as e:
        print(f"Invalid regex: {e}")
        return []
