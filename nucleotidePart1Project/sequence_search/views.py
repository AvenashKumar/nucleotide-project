from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import re
from django.conf import settings
from django.shortcuts import render
from django.core.cache import cache
import urllib.parse
from .services import fetch_sequence


def get_pattern(request):
    return request.GET.get('pattern') or request.POST.get('pattern') or ''

def search_pattern(request):
    matches = []
    pattern = get_pattern(request)
    sequence_id = settings.NCBI_EFETCH_ID
    sequence = fetch_sequence()

    if pattern:
        escaped_pattern = urllib.parse.quote(pattern, safe='')
        cache_key = f"pattern_matches::{sequence_id}::{escaped_pattern}"
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

            cache.set(cache_key, matches, timeout=settings.NCBI_SEQUENCE_CACHE_TIMEOUT)

    return render(request, 'sequence_search/search.html', {
        'pattern': pattern,
        'matches': matches,
        'sequence': sequence,
    })

@api_view(['GET'])
def pattern_search_api(request):
    pattern = request.GET.get('pattern', '').strip()
    sequence_id = settings.NCBI_EFETCH_ID
    sequence = fetch_sequence()

    if not pattern:
        return Response({
            'error': 'Missing "pattern" query parameter.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Sanitize cache key
    escaped_pattern = urllib.parse.quote(pattern, safe='')
    cache_key = f"pattern_matches::{sequence_id}::{escaped_pattern}"

    # Try to load from cache
    matches = cache.get(cache_key)

    if matches is None:
        try:
            regex = re.compile(pattern)
            matches = [{
                'start': m.start(),
                'end': m.end(),
                'match': m.group()
            } for m in regex.finditer(sequence)]
        except re.error as e:
            return Response({
                'error': f"Invalid regex pattern: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Store in cache
        cache.set(cache_key, matches, timeout=settings.NCBI_SEQUENCE_CACHE_TIMEOUT)

    return Response({
        'pattern': pattern,
        'matches': matches,
        'sequence': sequence
    })