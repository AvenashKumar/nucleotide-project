import re
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render

def fetch_sequence():

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nucleotide",
        "id": "30271926",
        "rettype": "fasta",
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        xml_root = ET.fromstring(response.text)
        tseq_sequence = xml_root.find('.//TSeq_sequence')
        sequence = tseq_sequence.text.strip().upper()
        return sequence
    return ""

def search_view(request):
    matches = []
    pattern = ''
    sequence = fetch_sequence()

    # Accept pattern from query parameter (GET) or form submission (POST)
    if request.method == 'GET':
        pattern = request.GET.get('pattern', '')
    elif request.method == 'POST':
        pattern = request.POST.get('pattern', '')

    if pattern:
        try:
            regex = re.compile(pattern)
            for match in regex.finditer(sequence):
                matches.append({
                    'start': match.start(),
                    'end': match.end(),
                    'match': match.group()
                })
        except re.error:
            matches.append({
                'start': -1,
                'end': -1,
                'match': "Invalid regular expression"
            })

    return render(request, 'sequence_search/search.html', {
        'pattern': pattern,
        'matches': matches,
        'sequence': sequence,
    })
