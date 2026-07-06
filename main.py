"""
main.py
-------
Entry point: parse the ForeFlight HTML navlog and generate a PDF from it.

Run:
    python3 main.py
"""

from navlog import parse_navlog
from create_pdf import build_pdf

INPUT_HTML = "ForeFlight Navlog.html"
OUTPUT_PDF = "Navlog.pdf"


def main():
    print(f"Parsing {INPUT_HTML} ...")
    data = parse_navlog(INPUT_HTML)

    print(f"  Route: {data['route']}")
    print(f"  Waypoints found: {len(data['waypoints'])}")
    print(f"  Winds aloft rows: {len(data['winds_aloft']['rows'])}")

    print(f"Building {OUTPUT_PDF} ...")
    build_pdf(data, OUTPUT_PDF)


if __name__ == "__main__":
    main()