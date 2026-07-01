#!/usr/bin/env python3
"""
harvest_mpm_woodcuts.py
=======================
Harvest all woodcut assets from the Museum Plantin-Moretus "Impressed by Plantin"
collection and build:

  mpm-woodcuts-manifest-uris.csv        — one row per asset
  mpm-woodcuts-collection.json          — IIIF Presentation 3 top-level Collection
  subcollections/
    mpm-woodcuts-subcollection-1.json
    mpm-woodcuts-subcollection-2.json
    …

Usage
-----
  cd /path/to/IIIF-manifest-samples/001-manifest-set/mpm-woodcuts
  python3 harvest_mpm_woodcuts.py

Optional flags
--------------
  --output-dir DIR     write output to DIR instead of cwd
  --resume             append to an existing CSV and skip already-seen UUIDs
  --dry-run            fetch pages and log progress, but write nothing to disk

API endpoint (confirmed 2026-06-30)
-------------------------------------
  https://dams1.antwerpen.be/api/v1/category/48351/assets.json?page=N
  Returns JSON:  { "header": {"count": "13793"}, "assets": [ {id, label, thumbnail, …}, … ] }
  Items per page: 50   |   Total items: ~13 793
"""

import argparse
import csv
import json
import logging
import math
import sys
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE        = "https://dams1.antwerpen.be/api/v1"
CATEGORY_ID     = 48351                      # "all-woodcuts" under impressedbyplantin
API_URL_TMPL    = f"{API_BASE}/category/{CATEGORY_ID}/assets.json?page={{page}}"

ITEMS_PER_API_PAGE  = 50                     # confirmed from live response
SUBCOLLECTION_SIZE  = 250
REQUEST_DELAY       = 0.4                    # seconds between page fetches
REQUEST_TIMEOUT     = 30                     # seconds per request
MAX_RETRIES         = 3                      # per page before giving up

PUBLIC_BASE = (
    "https://bretelemens.github.io/IIIF-manifest-samples"
    "/001-manifest-set/mpm-woodcuts"
)

TOP_COLLECTION_FILENAME = "mpm-woodcuts-collection.json"
CSV_FILENAME            = "mpm-woodcuts-manifest-uris.csv"
SUBCOLLECTIONS_DIRNAME  = "subcollections"

# Required keys that every harvested row must contain
REQUIRED_ROW_KEYS = {"asset_uuid", "manifest_uri", "iiif_image_uri"}

# ---------------------------------------------------------------------------
# IIIF metadata constants
# ---------------------------------------------------------------------------

PROVIDER = [
    {
        "id": "https://data.antwerpen.be/agent/museum-plantin-moretus",
        "type": "Agent",
        "label": {"nl": ["Museum Plantin-Moretus"]},
        "homepage": [
            {
                "id": "https://museumplantinmoretus.be/",
                "type": "Text",
                "label": {"nl": ["Homepage Museum Plantin-Moretus"]},
                "format": "text/html",
            }
        ],
    }
]

TOP_METADATA = [
    {"label": {"nl": ["naam"]},             "value": {"nl": ["Museum Plantin-Moretus – all woodcuts"]}},
    {"label": {"nl": ["identificatienummer"]},"value": {"nl": ["mpm-woodcuts"]}},
    {"label": {"nl": ["collectietype"]},    "value": {"nl": ["museale collectie"]}},
    {"label": {"nl": ["locatie"]},          "value": {"nl": ["Museum Plantin-Moretus"]}},
    {"label": {"nl": ["beheerder"]},        "value": {"nl": ["Stad Antwerpen, Museum Plantin-Moretus"]}},
    {"label": {"nl": ["acquisitiestatus"]}, "value": {"nl": ["actief"]}},
    {"label": {"nl": ["data-eigenaar"]},    "value": {"nl": ["Stad Antwerpen, Museum Plantin-Moretus"]}},
]

REQUIRED_STATEMENT = {
    "label": {"nl": ["Attribution"]},
    "value": {"nl": ["Stad Antwerpen, Museum Plantin-Moretus"]},
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (compatible; iiif-collection-builder/1.0; "
            "+https://github.com/bretelemens/IIIF-manifest-samples)"
        ),
        "Accept": "application/json",
        "Referer": "https://collectie.antwerpen.be/",
    })
    return s


def fetch_page(session: requests.Session, page: int) -> dict:
    """
    Fetch one API page and return the parsed JSON dict.
    Retries up to MAX_RETRIES times on transient errors (429, 5xx, timeout).
    Raises RuntimeError on persistent failure or unrecoverable HTTP status.
    """
    url = API_URL_TMPL.format(page=page)
    last_exc = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT)
        except requests.Timeout as exc:
            log.warning("  page %d attempt %d/%d – timeout (%s)", page, attempt, MAX_RETRIES, exc)
            last_exc = exc
            time.sleep(2 ** attempt)
            continue
        except requests.ConnectionError as exc:
            log.warning("  page %d attempt %d/%d – connection error (%s)", page, attempt, MAX_RETRIES, exc)
            last_exc = exc
            time.sleep(2 ** attempt)
            continue

        # --- HTTP status handling ---
        if resp.status_code == 200:
            try:
                return resp.json()
            except ValueError as exc:
                raise RuntimeError(
                    f"Page {page}: server returned HTTP 200 but body is not valid JSON. "
                    f"First 200 chars: {resp.text[:200]!r}"
                ) from exc

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 5))
            log.warning("  page %d – HTTP 429 rate-limited, waiting %ds", page, retry_after)
            time.sleep(retry_after)
            continue

        if resp.status_code in (500, 502, 503, 504):
            log.warning("  page %d attempt %d/%d – HTTP %d, retrying", page, attempt, MAX_RETRIES, resp.status_code)
            time.sleep(2 ** attempt)
            continue

        if resp.status_code == 404:
            # 404 on a page number means we've gone past the last page
            log.info("  page %d returned HTTP 404 – treating as end of results", page)
            return {}   # caller checks for empty assets list

        # Any other 4xx is unrecoverable
        resp.raise_for_status()

    raise RuntimeError(
        f"Page {page}: failed after {MAX_RETRIES} attempts. Last error: {last_exc}"
    )

# ---------------------------------------------------------------------------
# Data validation
# ---------------------------------------------------------------------------

MISSING_FIELD_LOG: list[dict] = []   # accumulated across all pages

def validate_row(raw: dict, page: int, position: int) -> dict | None:
    """
    Validate one raw API item and transform it into a row dict.
    Returns None and appends to MISSING_FIELD_LOG if any required source
    field is absent or empty.
    """
    asset_uuid = (raw.get("id") or "").strip()
    label      = (raw.get("label") or "").strip()

    missing = []
    if not asset_uuid:
        missing.append("id")
    if not label:
        missing.append("label")          # not required for CSV but worth logging

    if not asset_uuid:
        MISSING_FIELD_LOG.append({
            "page": page,
            "position": position,
            "missing_fields": missing,
            "raw_keys": list(raw.keys()),
        })
        return None

    return {
        "asset_uuid":    asset_uuid,
        "label":         label,
        "manifest_uri":  f"{PUBLIC_BASE}/manifests/{asset_uuid}.json",
        "iiif_image_uri": f"https://dams1.antwerpen.be/iiif/{asset_uuid}/full/full/0/default.jpg",
    }


def check_row_completeness(row: dict) -> list[str]:
    """Return list of missing required keys in a finalised row dict."""
    return [k for k in REQUIRED_ROW_KEYS if not row.get(k)]

# ---------------------------------------------------------------------------
# Harvest
# ---------------------------------------------------------------------------

def harvest_all_assets(session: requests.Session, resume_seen: set[str]) -> list[dict]:
    """
    Page through the full API and return a deduplicated, ordered list of row dicts.
    Skips UUIDs already in resume_seen (used for --resume mode).
    """
    rows: list[dict] = []
    seen: set[str] = set(resume_seen)

    # Fetch page 1 to discover total count
    log.info("Fetching page 1 to discover total item count …")
    data = fetch_page(session, 1)

    if not data or not data.get("assets"):
        raise RuntimeError(
            "Page 1 returned no assets. Check CATEGORY_ID or network connectivity. "
            f"Response keys: {list(data.keys()) if data else 'empty'}"
        )

    total_items  = int(data["header"]["count"])
    total_pages  = math.ceil(total_items / ITEMS_PER_API_PAGE)
    log.info("API reports %d total items → %d pages of %d", total_items, total_pages, ITEMS_PER_API_PAGE)

    # Process page 1 assets
    _process_page_assets(data["assets"], 1, seen, rows)

    # Pages 2 … N
    for page in range(2, total_pages + 1):
        log.info(
            "Page %d / %d  |  harvested so far: %d  |  skipped (resume): %d",
            page, total_pages, len(rows), len(resume_seen),
        )
        time.sleep(REQUEST_DELAY)
        data = fetch_page(session, page)

        assets = data.get("assets", [])
        if not assets:
            log.warning("Page %d returned 0 assets – stopping early", page)
            break

        _process_page_assets(assets, page, seen, rows)

    return rows


def _process_page_assets(
    assets: list[dict],
    page: int,
    seen: set[str],
    rows: list[dict],
) -> None:
    new_count = 0
    for i, raw in enumerate(assets):
        row = validate_row(raw, page, i)
        if row is None:
            continue                          # validation logged the issue

        uuid = row["asset_uuid"]
        if uuid in seen:
            continue                          # deduplicate
        seen.add(uuid)

        missing_keys = check_row_completeness(row)
        if missing_keys:
            log.warning("  asset %s is missing output fields: %s", uuid, missing_keys)

        rows.append(row)
        new_count += 1

    log.info("  → %d new assets from page %d", new_count, page)

# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

CSV_FIELDNAMES = ["asset_uuid", "label", "manifest_uri", "iiif_image_uri"]


def load_existing_csv(path: Path) -> set[str]:
    """Read existing CSV and return set of already-harvested UUIDs."""
    seen: set[str] = set()
    if not path.exists():
        return seen
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            uuid = (row.get("asset_uuid") or "").strip()
            if uuid:
                seen.add(uuid)
    log.info("Resume mode: loaded %d existing UUIDs from %s", len(seen), path)
    return seen


def append_rows_to_csv(path: Path, rows: list[dict], mode: str = "w") -> None:
    """
    Write (mode='w') or append (mode='a') rows to the CSV.
    Validates each row before writing; logs and skips incomplete rows.
    """
    write_header = (mode == "w") or (not path.exists())
    skipped = 0

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, mode, newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDNAMES, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        for row in rows:
            missing = check_row_completeness(row)
            if missing:
                log.warning(
                    "CSV: skipping row for %s – missing required fields: %s",
                    row.get("asset_uuid", "?"), missing,
                )
                skipped += 1
                continue
            writer.writerow(row)

    if skipped:
        log.warning("CSV: %d row(s) skipped due to missing required fields", skipped)
    log.info("CSV written: %s  (%d rows)", path, len(rows) - skipped)

# ---------------------------------------------------------------------------
# IIIF JSON builders
# ---------------------------------------------------------------------------

def thumbnail_for(asset_uuid: str) -> list[dict]:
    return [
        {
            "id": f"https://dams1.antwerpen.be/iiif/{asset_uuid}/full/full/0/default.jpg",
            "type": "Image",
            "format": "image/jpeg",
        }
    ]


def build_subcollection(
    sub_num: int,
    total_subs: int,
    total_items: int,
    page_rows: list[dict],
) -> dict:
    start     = (sub_num - 1) * SUBCOLLECTION_SIZE + 1
    end       = start + len(page_rows) - 1
    thumb_uuid = page_rows[0]["asset_uuid"] if page_rows else None

    sub_id  = f"{PUBLIC_BASE}/{SUBCOLLECTIONS_DIRNAME}/mpm-woodcuts-subcollection-{sub_num}.json"
    top_id  = f"{PUBLIC_BASE}/{TOP_COLLECTION_FILENAME}"

    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id":   sub_id,
        "type": "Collection",
        "partOf": [
            {
                "id":    top_id,
                "type":  "Collection",
                "label": {"nl": ["Museum Plantin-Moretus – all woodcuts"]},
            }
        ],
        "label":   {"nl": [f"MPM woodcuts – deel {sub_num}"]},
        "summary": {"nl": [f"Manifesten {start} tot {end} van {total_items} uit de set all woodcuts."]},
        "metadata": [
            {"label": {"nl": ["deelnummer"]},          "value": {"nl": [str(sub_num)]}},
            {"label": {"nl": ["totaal aantal delen"]}, "value": {"nl": [str(total_subs)]}},
            {"label": {"nl": ["aantal manifesten"]},   "value": {"nl": [str(len(page_rows))]}},
        ],
        "requiredStatement": REQUIRED_STATEMENT,
        "provider":  PROVIDER,
        "thumbnail": thumbnail_for(thumb_uuid) if thumb_uuid else [],
        "items": [
            {
                "id":    row["manifest_uri"],
                "type":  "Manifest",
                "label": {"nl": [row.get("label") or row["asset_uuid"]]},
            }
            for row in page_rows
        ],
    }


def build_top_collection(rows: list[dict], total_subs: int) -> dict:
    total_items = len(rows)
    top_items = []

    for sub_num in range(1, total_subs + 1):
        start = (sub_num - 1) * SUBCOLLECTION_SIZE + 1
        end   = min(sub_num * SUBCOLLECTION_SIZE, total_items)
        sub_id = f"{PUBLIC_BASE}/{SUBCOLLECTIONS_DIRNAME}/mpm-woodcuts-subcollection-{sub_num}.json"
        top_items.append(
            {
                "id":      sub_id,
                "type":    "Collection",
                "label":   {"nl": [f"MPM woodcuts – deel {sub_num}"]},
                "summary": {"nl": [f"Manifesten {start} tot {end} van {total_items}."]},
            }
        )

    thumb_uuid = rows[0]["asset_uuid"] if rows else None

    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id":   f"{PUBLIC_BASE}/{TOP_COLLECTION_FILENAME}",
        "type": "Collection",
        "label": {"nl": ["Museum Plantin-Moretus – all woodcuts"]},
        "summary": {
            "nl": [
                "Topcollectie met alle manifests voor de set all woodcuts, "
                f"opgesplitst in deelcollecties van {SUBCOLLECTION_SIZE}."
            ]
        },
        "metadata":          TOP_METADATA,
        "requiredStatement": REQUIRED_STATEMENT,
        "provider":          PROVIDER,
        "thumbnail":         thumbnail_for(thumb_uuid) if thumb_uuid else [],
        "items":             top_items,
    }

# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# Progress report
# ---------------------------------------------------------------------------

def print_harvest_report(
    rows: list[dict],
    total_subs: int,
    output_dir: Path,
    dry_run: bool,
) -> None:
    log.info("=" * 60)
    log.info("HARVEST COMPLETE")
    log.info("  Total assets harvested : %d", len(rows))
    log.info("  Sub-collections        : %d  (max %d items each)", total_subs, SUBCOLLECTION_SIZE)

    if MISSING_FIELD_LOG:
        log.warning("  Source manifest issues : %d item(s) skipped due to missing fields", len(MISSING_FIELD_LOG))
        for entry in MISSING_FIELD_LOG[:10]:      # show first 10
            log.warning(
                "    page=%d pos=%d missing=%s raw_keys=%s",
                entry["page"], entry["position"],
                entry["missing_fields"], entry["raw_keys"],
            )
        if len(MISSING_FIELD_LOG) > 10:
            log.warning("    … and %d more (full list not shown)", len(MISSING_FIELD_LOG) - 10)
    else:
        log.info("  Source manifest issues : none")

    if not dry_run:
        log.info("  Output directory       : %s", output_dir.resolve())
        log.info("  CSV file               : %s", output_dir / CSV_FILENAME)
        log.info("  Top collection         : %s", output_dir / TOP_COLLECTION_FILENAME)
        log.info("  Sub-collections dir    : %s", output_dir / SUBCOLLECTIONS_DIRNAME)
    else:
        log.info("  [dry-run] No files written.")
    log.info("=" * 60)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Harvest MPM woodcuts from the Antwerp DAMS API and build IIIF collections.",
    )
    p.add_argument(
        "--output-dir",
        default=None,
        help="Directory to write output files (default: current working directory).",
    )
    p.add_argument(
        "--resume",
        action="store_true",
        help="Load existing CSV and skip already-harvested UUIDs (append mode).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and validate data but do not write any files.",
    )
    return p.parse_args()

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args      = parse_args()
    output_dir = Path(args.output_dir) if args.output_dir else Path.cwd()
    csv_path   = output_dir / CSV_FILENAME

    log.info("MPM Woodcuts Harvester – starting")
    log.info("  API  : %s", API_URL_TMPL.format(page="N"))
    log.info("  Output dir: %s", output_dir.resolve())
    log.info("  Resume mode: %s  |  Dry-run: %s", args.resume, args.dry_run)

    # --- Resume: load already-seen UUIDs ---
    resume_seen: set[str] = set()
    if args.resume:
        resume_seen = load_existing_csv(csv_path)

    # --- Harvest ---
    session = make_session()
    rows    = harvest_all_assets(session, resume_seen)

    if not rows:
        log.error("No assets harvested. Aborting – no files will be written.")
        sys.exit(1)

    total_items = len(rows)
    total_subs  = math.ceil(total_items / SUBCOLLECTION_SIZE)

    # --- Write outputs ---
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / SUBCOLLECTIONS_DIRNAME).mkdir(parents=True, exist_ok=True)
        (output_dir / "manifests").mkdir(parents=True, exist_ok=True)

        # CSV
        csv_mode = "a" if args.resume else "w"
        append_rows_to_csv(csv_path, rows, mode=csv_mode)

        # Sub-collections
        for sub_num in range(1, total_subs + 1):
            start_idx = (sub_num - 1) * SUBCOLLECTION_SIZE
            end_idx   = start_idx + SUBCOLLECTION_SIZE
            page_rows = rows[start_idx:end_idx]

            sub = build_subcollection(sub_num, total_subs, total_items, page_rows)
            sub_path = output_dir / SUBCOLLECTIONS_DIRNAME / f"mpm-woodcuts-subcollection-{sub_num}.json"
            write_json(sub_path, sub)
            log.info("  wrote sub-collection %d / %d", sub_num, total_subs)

        # Top-level collection
        top = build_top_collection(rows, total_subs)
        write_json(output_dir / TOP_COLLECTION_FILENAME, top)

    print_harvest_report(rows, total_subs, output_dir, args.dry_run)


if __name__ == "__main__":
    main()
