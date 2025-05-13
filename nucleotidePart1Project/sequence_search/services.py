import requests
from django.conf import settings
import xml.etree.ElementTree as ET
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def fetch_sequence():
    cached = cache.get(settings.NCBI_SEQUENCE_CACHE_KEY)
    if cached:
        return cached

    try:
        response = requests.get(settings.NCBI_EFETCH_URL, params=settings.NCBI_EFETCH_PARAMS, timeout=10)
        response.raise_for_status()
        xml_root = ET.fromstring(response.text)
        tseq_sequence = xml_root.find('.//TSeq_sequence')
        if tseq_sequence is None:
            logger.warning("TSeq_sequence tag not found in XML.")
            return ""
        sequence = tseq_sequence.text.strip().upper()
        cache.set(settings.NCBI_SEQUENCE_CACHE_KEY, sequence, timeout=settings.NCBI_SEQUENCE_CACHE_TIMEOUT)
        return sequence
    except (requests.RequestException, ET.ParseError) as e:
        logger.error(f"Error fetching/parsing sequence: {e}")
        return ""
