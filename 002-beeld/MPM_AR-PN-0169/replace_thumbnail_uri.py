import json
import re
from copy import deepcopy
from pathlib import Path

THUMB_RE = re.compile(
    r"^https://media\.antwerpen\.be/media/18/c/([A-Za-z0-9]{24})/\1\.jpg$"
)

def transform_json(data):
    data = deepcopy(data)

    def walk(node):
        if isinstance(node, dict):
            resource_id = None
            images_obj = node.get("images")
            if isinstance(images_obj, dict):
                resource = images_obj.get("resource")
                if isinstance(resource, dict):
                    resource_id = resource.get("id")

            thumbnail = node.get("thumbnail")
            if isinstance(thumbnail, dict):
                thumb_id = thumbnail.get("id")
                if isinstance(thumb_id, str):
                    if THUMB_RE.match(thumb_id) and resource_id:
                        thumbnail["id"] = resource_id + "/full/175,/0/default.jpg"

            for value in node.values():
                walk(value)

        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return data

if __name__ == "__main__":
    input_file = Path.cwd() / "manifest-2.json"
    output_file = Path.cwd() / "manifest-2-transformed.json"

    with input_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    transformed = transform_json(data)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)

    print(f"Wrote transformed JSON to {output_file}")
