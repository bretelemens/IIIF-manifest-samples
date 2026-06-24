#!/usr/bin/env python3
import json
import re
import sys

PATTERN_OLD = re.compile(
    r'https://media\.antwerpen\.be/media/iiif/([A-Za-z0-9]{24})/canvas/normal'
)

BASE_NEW = (
    "https://bretelemens.github.io/IIIF-manifest-samples/"
    "002-beeld/MPM_AR-PN-0169/canvas/"
)

def is_sc_canvas_and_matching_id(obj):
    """
    Return True if:
      - obj is a dict
      - has "@type": "sc:Canvas"
      - has "@id" matching the old IIIF pattern
    """
    if not isinstance(obj, dict):
        return False

    at_type = obj.get("@type")
    if at_type != "sc:Canvas":
        return False

    if "@id" not in obj or not isinstance(obj["@id"], str):
        return False

    return PATTERN_OLD.match(obj["@id"])

def replace_uris_in_json(obj):
    counter = 1  # local to this function

    def build_new_dict(old_dict):
        new_dict = {}

        if is_sc_canvas_and_matching_id(old_dict):
            nonlocal counter
            old_uri = old_dict["@id"]
            new_uri = f"{BASE_NEW}{counter}"
            counter += 1
            # Insert "id" as first key
            new_dict["id"] = new_uri

        # Add all other keys in original order, skipping @id when replaced
        for key, val in old_dict.items():
            if key == "@id" and is_sc_canvas_and_matching_id(old_dict):
                continue  # skip original @id, we already added "id"

            if isinstance(val, dict):
                new_dict[key] = build_new_dict(val)
            elif isinstance(val, list):
                new_dict[key] = [
                    build_new_dict(item) if isinstance(item, dict) else item
                    for item in val
                ]
            else:
                new_dict[key] = val

        return new_dict

    def walk(node):
        if isinstance(node, dict):
            new_node = build_new_dict(node)
            node.clear()
            node.update(new_node)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(obj)

def process_json_file(input_path: str, output_path: str = None) -> None:
    if output_path is None:
        output_path = input_path + ".replaced"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    replace_uris_in_json(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Written JSON to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: replace_iiif_uris_sc_canvas.py input.json [output.json]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    process_json_file(input_file, output_file)
