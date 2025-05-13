import re
import requests
from django.conf import settings
import xml.etree.ElementTree as ET
from django.shortcuts import render
from django.core.cache import cache

def fetch_sequence():
    cached = cache.get(settings.NCBI_SEQUENCE_CACHE_KEY)
    if cached:
        return cached

    response = requests.get(settings.NCBI_EFETCH_URL, params=settings.NCBI_EFETCH_PARAMS)
    if response.status_code == 200:
        xml_root = ET.fromstring(response.text)
        tseq_sequence = xml_root.find('.//TSeq_sequence')
        sequence = tseq_sequence.text.strip().upper()

        cache.set(settings.NCBI_SEQUENCE_CACHE_KEY, sequence, timeout=settings.NCBI_SEQUENCE_CACHE_TIMEOUT)
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
