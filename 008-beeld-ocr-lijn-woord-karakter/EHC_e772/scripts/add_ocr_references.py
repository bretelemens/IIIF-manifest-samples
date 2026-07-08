"""
add_ocr_references.py — Add IIIF v3 annotations references and ALTO rendering
to a manifest.json, for canvases whose sequence number matches a page-{n}.json
file in the /ocr directory.

For each matching canvas the following nodes are added or updated:

    "annotations": [
        {
            "id": "{BASE_URI}/ocr/page-{n}.json",
            "type": "AnnotationPage"
        }
    ],
    "rendering": [
        {
            "id": "{BASE_URI}/alto/{alto_filename}",
            "type": "Text",
            "label": {"nl": ["ALTO weergave van de tekst van pagina {n}"]},
            "format": "application/xml"
        }
    ]

All existing rendering nodes on other canvases are removed.

The script also corrects the manifest base URI and all canvas/annotation URIs
from any legacy base path to the canonical 008-beeld-ocr-lijn-woord-karakter path.

Usage (run from the collection directory):
    python scripts/add_ocr_references.py \\
        --manifest manifest.json \\
        --ocr-dir ocr \\
        --alto-dir alto \\
        --output manifest.json \\
        --base-uri https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/EHC_e772

Arguments:
    --manifest   Path to the input manifest.json (default: manifest.json)
    --ocr-dir    Directory containing page-{n}.json files (default: ocr)
    --alto-dir   Directory containing ALTO xml files (default: alto)
    --output     Output path (default: manifest.json, overwrites in place)
    --base-uri   Canonical base URI for this collection
    --old-base   Legacy base URI to replace (auto-detected from manifest id if omitted)
"""

import argparse
import json
import re
import sys
from pathlib import Path

CANONICAL_BASE = (
    "https://bretelemens.github.io/IIIF-manifest-samples"
    "/008-beeld-ocr-lijn-woord-karakter/EHC_e772"
)


def collect_ocr_page_numbers(ocr_dir: Path) -> set:
    page_nrs = set()
    for f in ocr_dir.glob("page-*.json"):
        m = re.search(r"page-(\d+)\.json$", f.name)
        if m:
            page_nrs.add(int(m.group(1)))
    return page_nrs


def collect_alto_files(alto_dir: Path) -> dict:
    """Return mapping of sequence number -> filename for ALTO files."""
    alto_map = {}
    for f in alto_dir.glob("*.xml"):
        m = re.search(r"(\d+)\.xml$", f.name)
        if m:
            alto_map[int(m.group(1))] = f.name
    return alto_map


def fix_base_uri(content: str, old_base: str, new_base: str) -> tuple:
    count = content.count(old_base)
    return content.replace(old_base, new_base), count


def main():
    parser = argparse.ArgumentParser(
        description="Add OCR annotation references and ALTO rendering to a IIIF v3 manifest"
    )
    parser.add_argument("--manifest",  default="manifest.json")
    parser.add_argument("--ocr-dir",   default="ocr")
    parser.add_argument("--alto-dir",  default="alto")
    parser.add_argument("--output",    default="manifest.json")
    parser.add_argument("--base-uri",  default=CANONICAL_BASE)
    parser.add_argument("--old-base",  default=None,
                        help="Legacy base URI to replace (auto-detected if omitted)")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    ocr_dir       = Path(args.ocr_dir)
    alto_dir      = Path(args.alto_dir)
    output_path   = Path(args.output)
    base_uri      = args.base_uri

    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    # Step 1: fix base URI throughout the file (string replace before parsing)
    raw = manifest_path.read_text(encoding="utf-8")
    old_base = args.old_base or raw.split('"id"')[1].split('"')[1].rsplit("/", 1)[0]
    if old_base != base_uri:
        raw, n_replaced = fix_base_uri(raw, old_base, base_uri)
        print(f"Replaced base URI '{old_base}' -> '{base_uri}' ({n_replaced} occurrences)")
    else:
        print("Base URI already correct, no replacement needed")

    manifest = json.loads(raw)

    # Step 2: collect OCR page numbers and ALTO files
    ocr_page_nrs = collect_ocr_page_numbers(ocr_dir)
    alto_map     = collect_alto_files(alto_dir)
    print(f"OCR pages found:  {sorted(ocr_page_nrs)}")
    print(f"ALTO files found: {sorted(alto_map.keys())}")

    # Step 3: update canvases
    annotations_added = 0
    rendering_removed = 0
    rendering_added   = 0

    for i, canvas in enumerate(manifest["items"], start=1):
        # Remove all existing rendering nodes
        if "rendering" in canvas:
            del canvas["rendering"]
            rendering_removed += 1

        if i in ocr_page_nrs:
            # Add annotations reference
            canvas["annotations"] = [
                {
                    "id":   f"{base_uri}/ocr/page-{i}.json",
                    "type": "AnnotationPage",
                }
            ]
            annotations_added += 1

        if i in alto_map:
            # Add ALTO rendering
            canvas["rendering"] = [
                {
                    "id":     f"{base_uri}/alto/{alto_map[i]}",
                    "type":   "Text",
                    "label":  {"nl": [f"ALTO weergave van de tekst van pagina {i}"]},
                    "format": "application/xml",
                }
            ]
            rendering_added += 1

    output_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Rendering removed:    {rendering_removed}")
    print(f"Annotations added:    {annotations_added} (canvases {sorted(ocr_page_nrs)})")
    print(f"ALTO rendering added: {rendering_added} (canvases {sorted(alto_map.keys())})")
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
