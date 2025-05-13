import argparse
from nucleotide_search import fetch_sequence, search_pattern

# -----------------------------
# CLI Entry Point
# -----------------------------

DEFAULT_NCBI_EFETCH_ID = "224589800"


def main():
    parser = argparse.ArgumentParser(description="Search regex pattern in NCBI nucleotide sequence")
    parser.add_argument('pattern', type=str, help='Regex pattern to search')
    parser.add_argument('--id', type=str, default=DEFAULT_NCBI_EFETCH_ID,
                        help='NCBI nucleotide sequence ID (default: 30271926)')
    parser.add_argument('--no-cache', action='store_true', help='Disable Memcached usage')
    args = parser.parse_args()

    print("Fetching nucleotide sequence...")
    sequence = fetch_sequence(args.id, use_cache=not args.no_cache)

    print(f"Searching for pattern: {args.pattern}")
    matches = search_pattern(sequence, args.pattern, args.id)

    print(f"Sequence Length: {len(sequence)}")
    print(f"Matches Found: {len(matches)}\n")

    for i, m in enumerate(matches, 1):
        print(f"{i:2}. {m['match']} (from {m['start']} to {m['end']})")

    if not matches:
        print("No matches found.")

if __name__ == '__main__':
    main()