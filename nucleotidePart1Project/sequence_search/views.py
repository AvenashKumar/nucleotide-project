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
    sequence_id = settings.NCBI_EFETCH_ID
    sequence = fetch_sequence()

    if request.method == 'GET':
        pattern = request.GET.get('pattern', '')
    elif request.method == 'POST':
        pattern = request.POST.get('pattern', '')

    if pattern:
        cache_key = f"pattern_matches::{sequence_id}::{pattern}"
        matches = cache.get(cache_key)

        if matches is None:
            try:
                regex = re.compile(pattern)
                matches = [{
                    'start': match.start(),
                    'end': match.end(),
                    'match': match.group()
                } for match in regex.finditer(sequence)]

            except re.error:
                matches = [{
                    'start': -1,
                    'end': -1,
                    'match': "Invalid regular expression"
                }]

            # Cache the result for 10 minutes (600 seconds)
            cache.set(cache_key, matches, timeout=600)

    return render(request, 'sequence_search/search.html', {
        'pattern': pattern,
        'matches': matches,
        'sequence': sequence,
    })
