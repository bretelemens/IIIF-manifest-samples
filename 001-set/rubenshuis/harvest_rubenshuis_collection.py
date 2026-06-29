#!/usr/bin/env python3

import json
import csv
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

BASE_API = "https://dams.antwerpen.be/api/lod-search"
PUBLISHER = "Rubenshuis"

COLLECTION_UUID = "rubenshuis-sample-collection"
COLLECTION_ID = f"https://dams.antwerpen.be/iiif/collection/{COLLECTION_UUID}/manifest"
MANIFEST_BASE = "https://dams.antwerpen.be/iiif"

OUTPUT_COLLECTION = "rubenshuis-collection.json"
OUTPUT_CSV = "rubenshuis-manifest-uris.csv"

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
                "format": "text/html",
            }
        ],
        "logo": [
            {
                "id": "https://www.antwerpen.be/assets/images/logos/logo_A_stad_antwerpen.png",
                "type": "Image",
                "format": "image/png",
            }
        ],
    }
]

METADATA = [
    {"label": {"nl": ["naam"]}, "value": {"nl": ["Collectie Rubenshuis"]}},
    {"label": {"nl": ["identificatienummer"]}, "value": {"nl": [COLLECTION_UUID]}},
    {"label": {"nl": ["collectietype"]}, "value": {"nl": ["museale collectie"]}},
    {"label": {"nl": ["locatie"]}, "value": {"nl": ["Rubenshuis"]}},
    {"label": {"nl": ["beheerder"]}, "value": {"nl": ["Stad Antwerpen, Rubenshuis"]}},
    {"label": {"nl": ["acquisitiestatus"]}, "value": {"nl": ["actief"]}},
    {"label": {"nl": ["data-eigenaar"]}, "value": {"nl": ["Stad Antwerpen, Rubenshuis"]}},
]

REQUIRED_STATEMENT = {
    "label": {"nl": ["Attribution"]},
    "value": {"nl": ["Stad Antwerpen, Rubenshuis"]},
}


def text_of_child(elem, name):
    child = elem.find(name)
    return child.text.strip() if child is not None and child.text else ""


def harvest_rubenshuis_assets():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 iiif-harvester"})

    rows = []
    items = []
    seen = set()
    thumb_uuid = None

    limit = 200
    offset = 0

    while True:
        url = f"{BASE_API}?{urlencode({'publisher': PUBLISHER, 'limit': limit, 'offset': offset})}"
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

            manifest_uri = f"{MANIFEST_BASE}/{asset_uuid}/manifest.json"

            items.append(
                {
                    "id": manifest_uri,
                    "type": "Manifest",
                    "label": {"nl": [title]},
                }
            )

            rows.append(
                {
                    "asset_uuid": asset_uuid,
                    "title": title,
                    "identifier": identifier,
                    "publisher": publisher,
                    "manifest_uri": manifest_uri,
                }
            )

            if thumb_uuid is None:
                thumb_uuid = asset_uuid

        if len(results) < limit:
            break

        offset += limit

    return rows, items, thumb_uuid


def build_collection(items, thumb_uuid):
    thumbnail = []
    if thumb_uuid:
        thumbnail = [
            {
                "id": f"https://dams.antwerpen.be/iiif/{thumb_uuid}/full/max/0/default.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "service": [
                    {
                        "id": f"https://dams.antwerpen.be/iiif/{thumb_uuid}",
                        "type": "ImageService3",
                        "profile": "level0",
                    }
                ],
            }
        ]

    collection = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": COLLECTION_ID,
        "type": "Collection",
        "label": {"nl": ["Collectie Rubenshuis"]},
        "summary": {
            "nl": [
                "Verzameling van manifestverwijzingen voor assets uit DAMS Antwerpen met publisher Rubenshuis."
            ]
        },
        "metadata": METADATA,
        "requiredStatement": REQUIRED_STATEMENT,
        "provider": PROVIDER,
        "thumbnail": thumbnail,
        "items": items,
    }

    return collection


def write_csv(rows, filename):
    with open(filename, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["asset_uuid", "title", "identifier", "publisher", "manifest_uri"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_json(data, filename):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def main():
    rows, items, thumb_uuid = harvest_rubenshuis_assets()
    collection = build_collection(items, thumb_uuid)

    write_csv(rows, OUTPUT_CSV)
    write_json(collection, OUTPUT_COLLECTION)

    print(f"Harvested {len(rows)} Rubenshuis assets")
    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {OUTPUT_COLLECTION}")


if __name__ == "__main__":
    main()
