import json
import re
from pathlib import Path

OCR_DIR = Path("ocr")
BASE_URI = "https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34/ocr"

FILE_RE = re.compile(r"^page-(\d+)\.json$")

for path in OCR_DIR.glob("page-*.json"):
    match = FILE_RE.match(path.name)
    if not match:
        continue

    page_no = match.group(1)

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    data["id"] = f"{BASE_URI}/page-{page_no}"

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {path} -> {data['id']}")
