#!/usr/bin/env python3

import csv
import json
import math
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode

BASE_API = "https://dams.antwerpen.be/api/lod-search"
PUBLISHER = "Rubenshuis"
API_PAGE_SIZE = 200
SUBCOLLECTION_SIZE = 250

# Write everything in the directory where the script is launched.
OUTPUT_DIR = Path.cwd()

# Public base URI for the files as they will be published.
# Change this if your GitHub Pages path is different.
PUBLIC_BASE = "https://bretelemens.github.io/IIIF-manifest-samples/001-set/rubenshuis"

TOP_COLLECTION_FILENAME = "rubenshuis-collection.json"
CSV_FILENAME = "rubenshuis-manifest-uris.csv"
SUBCOLLECTIONS_DIRNAME = "subcollections"

PROVIDER = [
    {
        "id": "https://data.antwerpen.be/agent/rubenshuis",
        "type": "Agent",
        "label": {"nl": ["Rubenshuis"]},
        "homepage": [
            {
                "id": "https://rubenshuis.be/",
                "type": "Text",
                "label": {"nl": ["Homepage Rubenshuis"]},
                "format": "text/html"
            }
        ],
        "logo": [
            {
                "id": "https://www.antwerpen.be/assets/images/logos/logo_A_stad_antwerpen.png",
                "type": "Image",
                "format": "image/png"
            }
        ]
    }
]

TOP_METADATA = [
    {"label": {"nl": ["naam"]}, "value": {"nl": ["Collectie Rubenshuis"]}},
    {"label": {"nl": ["identificatienummer"]}, "value": {"nl": ["rubenshuis"]}},
    {"label": {"nl": ["collectietype"]}, "value": {"nl": ["museale collectie"]}},
    {"label": {"nl": ["locatie"]}, "value": {"nl": ["Rubenshuis"]}},
    {"label": {"nl": ["beheerder"]}, "value": {"nl": ["Stad Antwerpen, Rubenshuis"]}},
    {"label": {"nl": ["acquisitiestatus"]}, "value": {"nl": ["actief"]}},
    {"label": {"nl": ["data-eigenaar"]}, "value": {"nl": ["Stad Antwerpen, Rubenshuis"]}}
]

REQUIRED_STATEMENT = {
    "label": {"nl": ["Attribution"]},
    "value": {"nl": ["Stad Antwerpen, Rubenshuis"]}
}


def text_of_child(elem, name):
    child = elem.find(name)
    return child.text.strip() if child is not None and child.text else ""


def thumbnail_for(asset_uuid):
    return [
        {
            "id": f"https://dams.antwerpen.be/iiif/{asset_uuid}/full/max/0/default.jpg",
            "type": "Image",
            "format": "image/jpeg",
            "service": [
                {
                    "id": f"https://dams.antwerpen.be/iiif/{asset_uuid}",
                    "type": "ImageService3",
                    "profile": "level0"
                }
            ]
        }
    ]


def harvest_assets():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 iiif-harvester"})

    rows = []
    seen = set()
    offset = 0

    while True:
        url = f"{BASE_API}?{urlencode({'publisher': PUBLISHER, 'limit': API_PAGE_SIZE, 'offset': offset})}"
        response = session.get(url, timeout=60)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        results = root.findall("result")

        if not results:
            break

        for result in results:
            asset_uuid = (result.attrib.get("id") or "").strip()
            if not asset_uuid or asset_uuid in seen:
                continue

            seen.add(asset_uuid)

            title = text_of_child(result, "title") or "Zonder titel"
            identifier = text_of_child(result, "identifier")
            publisher = text_of_child(result, "publisher")

            manifest_uri = f"{PUBLIC_BASE}/manifests/{asset_uuid}.json"

            rows.append({
                "asset_uuid": asset_uuid,
                "title": title,
                "identifier": identifier,
                "publisher": publisher,
                "manifest_uri": manifest_uri
            })

        if len(results) < API_PAGE_SIZE:
            break

        offset += API_PAGE_SIZE

    return rows


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["asset_uuid", "title", "identifier", "publisher", "manifest_uri"]
        )
        writer.writeheader()
        writer.writerows(rows)


def build_subcollection(page_num, total_pages, total_items, page_rows):
    start = ((page_num - 1) * SUBCOLLECTION_SIZE) + 1
    end = start + len(page_rows) - 1
    thumb_uuid = page_rows[0]["asset_uuid"] if page_rows else None

    subcollection_id = f"{PUBLIC_BASE}/{SUBCOLLECTIONS_DIRNAME}/rubenshuis-subcollection-{page_num}.json"
    top_collection_id = f"{PUBLIC_BASE}/{TOP_COLLECTION_FILENAME}"

    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": subcollection_id,
        "type": "Collection",
        "partOf": [
            {
                "id": top_collection_id,
                "type": "Collection",
                "label": {"nl": ["Collectie Rubenshuis"]}
            }
        ],
        "label": {"nl": [f"Collectie Rubenshuis – deel {page_num}"]},
        "summary": {
            "nl": [f"Manifesten {start} tot {end} van {total_items} uit de Rubenshuis-collectie."]
        },
        "metadata": [
            {"label": {"nl": ["deelnummer"]}, "value": {"nl": [str(page_num)]}},
            {"label": {"nl": ["totaal aantal delen"]}, "value": {"nl": [str(total_pages)]}},
            {"label": {"nl": ["aantal manifesten"]}, "value": {"nl": [str(len(page_rows))]}}
        ],
        "requiredStatement": REQUIRED_STATEMENT,
        "provider": PROVIDER,
        "thumbnail": thumbnail_for(thumb_uuid) if thumb_uuid else [],
        "items": [
            {
                "id": row["manifest_uri"],
                "type": "Manifest",
                "label": {"nl": [row["title"]]}
            }
            for row in page_rows
        ]
    }


def build_top_collection(rows, total_pages):
    top_items = []

    for page_num in range(1, total_pages + 1):
        subcollection_id = f"{PUBLIC_BASE}/{SUBCOLLECTIONS_DIRNAME}/rubenshuis-subcollection-{page_num}.json"
        start = ((page_num - 1) * SUBCOLLECTION_SIZE) + 1
        end = min(page_num * SUBCOLLECTION_SIZE, len(rows))

        top_items.append({
            "id": subcollection_id,
            "type": "Collection",
            "label": {"nl": [f"Collectie Rubenshuis – deel {page_num}"]},
            "summary": {"nl": [f"Manifesten {start} tot {end} van {len(rows)}."]}
        })

    thumb_uuid = rows[0]["asset_uuid"] if rows else None

    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{PUBLIC_BASE}/{TOP_COLLECTION_FILENAME}",
        "type": "Collection",
        "label": {"nl": ["Collectie Rubenshuis"]},
        "summary": {
            "nl": ["Topcollectie voor Rubenshuis met verwijzingen naar deelcollecties van telkens 250 manifesten."]
        },
        "metadata": TOP_METADATA,
        "requiredStatement": REQUIRED_STATEMENT,
        "provider": PROVIDER,
        "thumbnail": thumbnail_for(thumb_uuid) if thumb_uuid else [],
        "items": top_items
    }


def main():
    rows = harvest_assets()
    total_items = len(rows)
    total_pages = math.ceil(total_items / SUBCOLLECTION_SIZE)

    write_csv(OUTPUT_DIR / CSV_FILENAME, rows)

    subcollections_dir = OUTPUT_DIR / SUBCOLLECTIONS_DIRNAME
    subcollections_dir.mkdir(parents=True, exist_ok=True)

    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * SUBCOLLECTION_SIZE
        end_idx = start_idx + SUBCOLLECTION_SIZE
        page_rows = rows[start_idx:end_idx]

        subcollection = build_subcollection(page_num, total_pages, total_items, page_rows)
        subcollection_path = subcollections_dir / f"rubenshuis-subcollection-{page_num}.json"
        write_json(subcollection_path, subcollection)

    top_collection = build_top_collection(rows, total_pages)
    write_json(OUTPUT_DIR / TOP_COLLECTION_FILENAME, top_collection)

    print(f"Harvested {total_items} manifests")
    print(f"Wrote top-level collection: {OUTPUT_DIR / TOP_COLLECTION_FILENAME}")
    print(f"Wrote sub-Collections in: {subcollections_dir}")
    print(f"Wrote CSV manifest list: {OUTPUT_DIR / CSV_FILENAME}")


if __name__ == "__main__":
    main()
