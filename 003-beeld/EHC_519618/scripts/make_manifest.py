"""
make_manifest.py — Generate a IIIF Presentation API v3 manifest.json
from a legacy IIIF v2 source.json for EHC_519618.

Usage:
    python scripts/make_manifest.py \
        --source source.json \
        --output manifest.json

The script reads the legacy v2 manifest (source.json), converts each canvas
to IIIF v3, strips TIFF renderings, and injects descriptive metadata.
"""

import argparse
import json
import sys
from pathlib import Path

BASE_URI = (
    "https://bretelemens.github.io/IIIF-manifest-samples/003-beeld/EHC_519618"
)

METADATA = [
    {
        "label": {"nl": ["Inventarisnummer"]},
        "value": {"nl": ["519618 [S4-92 b]"]},
    },
    {
        "label": {"nl": ["Titel"]},
        "value": {
            "nl": [
                "Antwerpsch straatnamenboek : lijst van al de straatnamen, "
                "oude en nieuwe, met hun beteekenis, reden, oorsprong en veranderingen"
            ]
        },
    },
    {
        "label": {"nl": ["Auteur"]},
        "value": {"nl": ["Prims, Floris; Verbeeck, Michel"]},
    },
    {
        "label": {"nl": ["Uitgave"]},
        "value": {"nl": ["Antwerpen : Boekhandel der \"Bijdragen\", 1926"]},
    },
    {
        "label": {"nl": ["Datering"]},
        "value": {"nl": ["1926"]},
    },
    {
        "label": {"nl": ["Taal"]},
        "value": {"nl": ["Nederlands"]},
    },
    {
        "label": {"nl": ["Omvang"]},
        "value": {"nl": ["352 p."]},
    },
    {
        "label": {"nl": ["Type"]},
        "value": {"nl": ["Woordenboek. Repertorium"]},
    },
    {
        "label": {"nl": ["Onderwerp"]},
        "value": {"nl": ["stratengidsen; Antwerpen"]},
    },
    {
        "label": {"nl": ["Bewaarinstelling"]},
        "value": {"nl": ["Erfgoedbibliotheek Hendrik Conscience, Antwerpen"]},
    },
    {
        "label": {"nl": ["Collectie"]},
        "value": {
            "nl": [
                "Collectie digitale publicaties van de Erfgoedbibliotheek Hendrik Conscience"
            ]
        },
    },
    {
        "label": {"nl": ["Permalink"]},
        "value": {
            "nl": [
                '<a href="https://go.wander.be/record/opacehc/c:lvd:133484">'
                "https://go.wander.be/record/opacehc/c:lvd:133484</a>"
            ]
        },
    },
]


def convert_canvas(src_canvas: dict, index: int) -> dict:
    """Convert a single IIIF v2 canvas to IIIF v3."""
    img = src_canvas["images"][0]
    svc_id = img["resource"]["service"]["@id"]
    height = src_canvas["height"]
    width = src_canvas["width"]
    thumb = src_canvas["thumbnail"]["@id"]

    # Keep only XML (ALTO) renderings, drop TIFF
    rendering = []
    for r in src_canvas.get("rendering", []):
        if r["format"] == "application/xml":
            rendering.append(
                {
                    "id": r["@id"],
                    "type": "Text",
                    "label": {"nl": [r["label"]]},
                    "format": "application/xml",
                }
            )

    canvas = {
        "id": f"{BASE_URI}/canvas/{index}",
        "type": "Canvas",
        "label": {"nl": [f"scan-{index}"]},
        "height": height,
        "width": width,
        "items": [
            {
                "id": f"{BASE_URI}/page/{index}/1",
                "type": "AnnotationPage",
                "items": [
                    {
                        "id": f"{BASE_URI}/annotation/{index}/1/1",
                        "type": "Annotation",
                        "motivation": "painting",
                        "body": {
                            "id": f"{svc_id}/full/max/0/default.jpg",
                            "type": "Image",
                            "format": "image/jpeg",
                            "height": height,
                            "width": width,
                            "service": [
                                {
                                    "id": svc_id,
                                    "type": "ImageService2",
                                    "profile": "level2",
                                }
                            ],
                        },
                        "target": f"{BASE_URI}/canvas/{index}",
                    }
                ],
            }
        ],
        "thumbnail": [
            {
                "id": thumb,
                "type": "Image",
                "format": "image/jpeg",
            }
        ],
    }

    if rendering:
        canvas["rendering"] = rendering

    return canvas


def build_manifest(source_path: Path) -> dict:
    with open(source_path, encoding="utf-8") as f:
        src = json.load(f)

    src_canvases = src["sequences"][0]["canvases"]
    items = [convert_canvas(c, i) for i, c in enumerate(src_canvases, start=1)]

    manifest = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{BASE_URI}/manifest.json",
        "type": "Manifest",
        "label": {
            "nl": [
                "Antwerpsch straatnamenboek : lijst van al de straatnamen, "
                "oude en nieuwe, met hun beteekenis, reden, oorsprong en veranderingen"
            ]
        },
        "summary": {
            "nl": [
                "Antwerpsch straatnamenboek van Floris Prims en Michel Verbeeck. "
                "Antwerpen : Boekhandel der \"Bijdragen\", 1926. 352 p. "
                "Woordenboek van alle Antwerpse straatnamen, oud en nieuw, "
                "met hun betekenis, reden, oorsprong en veranderingen."
            ]
        },
        "metadata": METADATA,
        "viewingDirection": "left-to-right",
        "behavior": ["paged"],
        "provider": [
            {
                "id": "https://www.wikidata.org/entity/Q1954501",
                "type": "Agent",
                "label": {"nl": ["Erfgoedbibliotheek Hendrik Conscience"]},
                "homepage": [
                    {
                        "id": "https://erfgoedbibliotheek.antwerpen.be/",
                        "type": "Text",
                        "label": {
                            "nl": [
                                "Homepage Erfgoedbibliotheek Hendrik Conscience"
                            ]
                        },
                        "format": "text/html",
                    }
                ],
            }
        ],
        "rights": "http://creativecommons.org/publicdomain/mark/1.0/",
        "requiredStatement": {
            "label": {"nl": ["Naamsvermelding"]},
            "value": {
                "nl": [
                    "519618, Collectie Stad Antwerpen, "
                    "Erfgoedbibliotheek Hendrik Conscience"
                ]
            },
        },
        "thumbnail": [
            {
                "id": src_canvases[0]["thumbnail"]["@id"],
                "type": "Image",
                "format": "image/jpeg",
            }
        ],
        "seeAlso": [
            {
                "id": "https://go.wander.be/record/opacehc/c:lvd:133484",
                "type": "Dataset",
                "label": {
                    "nl": ["Catalogusrecord Erfgoedbibliotheek Hendrik Conscience"]
                },
                "format": "text/html",
            }
        ],
        "items": items,
    }

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Convert legacy v2 source.json to IIIF v3 manifest.json")
    parser.add_argument("--source", default="source.json", help="Path to source.json")
    parser.add_argument("--output", default="manifest.json", help="Output path")
    args = parser.parse_args()

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"ERROR: source file not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    manifest = build_manifest(source_path)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Written: {args.output} ({len(manifest['items'])} canvases)")


if __name__ == "__main__":
    main()
