from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import render
from .services import fetch_sequence, get_pattern_matches, get_pattern


def search_pattern(request):
    pattern = get_pattern(request)
    sequence = fetch_sequence()
    sequence_id = settings.NCBI_EFETCH_ID
    matches = []

    if pattern:
        matches, _ = get_pattern_matches(pattern, sequence, sequence_id)

    return render(request, 'sequence_search/search.html', {
        'pattern': pattern,
        'matches': matches,
        'sequence': sequence,
    })

@api_view(['GET'])
def pattern_search_api(request):
    pattern = request.GET.get('pattern', '').strip()
    if not pattern:
        return Response({
            'error': 'Missing "pattern" query parameter.'
        }, status=status.HTTP_400_BAD_REQUEST)

    sequence = fetch_sequence()
    sequence_id = settings.NCBI_EFETCH_ID

    matches, error = get_pattern_matches(pattern, sequence, sequence_id)

    if error:
        return Response({
            'error': str(error)
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'pattern': pattern,
        'matches': matches,
        'sequence': sequence
    })
