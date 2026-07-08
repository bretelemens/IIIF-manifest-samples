"""
add_ocr_references.py — Add IIIF v3 annotations references to a manifest.json,
pointing to corresponding AnnotationPage files in the /ocr directory.

For each canvas whose sequence number matches a page-{n}.json file in /ocr,
an "annotations" node is added:

    "annotations": [
        {
            "id": "{BASE_URI}/ocr/page-{n}.json",
            "type": "AnnotationPage"
        }
    ]

The canvas sequence number is its 1-based position in the manifest items list.

Usage (run from the collection directory):
    python scripts/add_ocr_references.py \\
        --manifest manifest.json \\
        --ocr-dir ocr \\
        --output manifest.json

Arguments:
    --manifest   Path to the input manifest.json (default: manifest.json)
    --ocr-dir    Path to the directory containing page-{n}.json files (default: ocr)
    --output     Path for the output manifest.json (default: manifest.json, overwrites in place)
    --base-uri   Base URI for the collection. If omitted, derived from the manifest id.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def derive_base_uri(manifest_id: str) -> str:
    """Strip the filename from the manifest id to get the base URI."""
    return manifest_id.rsplit("/", 1)[0]


def collect_ocr_page_numbers(ocr_dir: Path) -> set[int]:
    """Return the set of page numbers for which an OCR file exists."""
    page_nrs = set()
    for f in ocr_dir.glob("page-*.json"):
        m = re.search(r"page-(\d+)\.json$", f.name)
        if m:
            page_nrs.add(int(m.group(1)))
    return page_nrs


def add_ocr_references(manifest: dict, ocr_page_nrs: set[int], base_uri: str) -> tuple[dict, int]:
    """
    Add annotations nodes to canvases whose sequence number is in ocr_page_nrs.
    Returns the updated manifest and a count of canvases updated.
    """
    updated = 0
    for i, canvas in enumerate(manifest["items"], start=1):
        if i in ocr_page_nrs:
            canvas["annotations"] = [
                {
                    "id": f"{base_uri}/ocr/page-{i}.json",
                    "type": "AnnotationPage",
                }
            ]
            updated += 1
    return manifest, updated


def main():
    parser = argparse.ArgumentParser(
        description="Add OCR annotation page references to a IIIF v3 manifest"
    )
    parser.add_argument("--manifest", default="manifest.json", help="Input manifest.json")
    parser.add_argument("--ocr-dir", default="ocr", help="Directory with page-{n}.json files")
    parser.add_argument("--output", default="manifest.json", help="Output manifest.json (default: overwrite in place)")
    parser.add_argument("--base-uri", default=None, help="Base URI (derived from manifest id if omitted)")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    ocr_dir = Path(args.ocr_dir)
    output_path = Path(args.output)

    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)
    if not ocr_dir.exists():
        print(f"ERROR: ocr directory not found: {ocr_dir}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    base_uri = args.base_uri or derive_base_uri(manifest["id"])
    ocr_page_nrs = collect_ocr_page_numbers(ocr_dir)

    if not ocr_page_nrs:
        print("WARNING: no page-{n}.json files found in ocr directory", file=sys.stderr)

    print(f"Manifest: {manifest_path} ({len(manifest['items'])} canvases)")
    print(f"Base URI: {base_uri}")
    print(f"OCR pages found: {sorted(ocr_page_nrs)}")

    manifest, updated = add_ocr_references(manifest, ocr_page_nrs, base_uri)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated} canvas(es) with annotations reference")
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
