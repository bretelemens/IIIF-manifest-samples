"""
embed_annotations.py

Reads manifest.json and, for each canvas, replaces the stub annotation page
reference in the `annotations` node with the full content of the corresponding
ocr/page-{n}.json file.  Writes the result to embedded-manifest.json.

Usage:
    python embed_annotations.py [manifest_in] [ocr_dir] [manifest_out]

Defaults:
    manifest_in  = manifest.json
    ocr_dir      = ocr/
    manifest_out = embedded-manifest.json
"""

import json
import sys
from pathlib import Path


def embed_annotations(manifest_in: Path, ocr_dir: Path, manifest_out: Path) -> None:
    with manifest_in.open(encoding="utf-8") as f:
        manifest = json.load(f)

    embedded = 0
    missing = []

    for i, canvas in enumerate(manifest.get("items", []), start=1):
        annotations = canvas.get("annotations", [])
        if not annotations:
            continue

        # Load the corresponding OCR page file
        ocr_file = ocr_dir / f"page-{i}.json"
        if not ocr_file.exists():
            missing.append(str(ocr_file))
            continue

        with ocr_file.open(encoding="utf-8") as f:
            ocr_page = json.load(f)

        # Replace the stub with the full AnnotationPage content.
        # We preserve the id and type from the stub, adding items (and
        # any other fields) from the OCR file.
        stub = annotations[0]
        full_ap = {
            "id":   stub.get("id", ocr_page.get("id")),
            "type": "AnnotationPage",
        }
        # Copy all keys from the OCR file except @context (not needed when embedded)
        for key, value in ocr_page.items():
            if key not in ("@context", "id", "type"):
                full_ap[key] = value

        canvas["annotations"] = [full_ap]
        embedded += 1

    with manifest_out.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Embedded {embedded} annotation page(s) into {manifest_out}")
    if missing:
        print(f"Warning: {len(missing)} OCR file(s) not found:")
        for p in missing:
            print(f"  {p}")


if __name__ == "__main__":
    base = Path(__file__).parent
    manifest_in  = Path(sys.argv[1]) if len(sys.argv) > 1 else base / "manifest.json"
    ocr_dir      = Path(sys.argv[2]) if len(sys.argv) > 2 else base / "ocr"
    manifest_out = Path(sys.argv[3]) if len(sys.argv) > 3 else base / "embedded-manifest.json"

    embed_annotations(manifest_in, ocr_dir, manifest_out)
