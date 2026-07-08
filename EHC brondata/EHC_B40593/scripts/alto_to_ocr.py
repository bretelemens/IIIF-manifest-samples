"""
alto_to_ocr.py

Transform a directory of ALTO XML files into IIIF Web Annotation JSON files
using a local XSLT 1.0 stylesheet (transform.xsl).

Requires: lxml

Usage:
    python alto_to_ocr.py [options]

Options:
    --alto-dir   DIR    Directory containing ALTO XML files (default: ../alto)
    --ocr-dir    DIR    Output directory for JSON files (default: ../ocr)
    --xsl        FILE   Path to the XSLT stylesheet (default: transform.xsl)
    --base-uri   URI    Base URI for the collection (overrides value in XSL)
    --x-ratio    N      X scaling ratio (overrides value in XSL, default: 1)
    --y-ratio    N      Y scaling ratio (overrides value in XSL, default: 1)
    --pattern    GLOB   Filename glob for ALTO files (default: HKW_M34_*.xml)
    --dry-run           Parse and transform but do not write output files

Example:
    python scripts/alto_to_ocr.py \\
        --alto-dir alto \\
        --ocr-dir ocr \\
        --xsl scripts/transform.xsl \\
        --base-uri https://bretelemens.github.io/IIIF-manifest-samples/008-beeld-ocr-lijn-woord-karakter/momu-m34
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    sys.exit("lxml is required. Install it with: pip install lxml")


def parse_args():
    script_dir = Path(__file__).parent
    repo_dir   = script_dir.parent

    p = argparse.ArgumentParser(
        description="Transform ALTO XML files to IIIF AnnotationPage JSON using XSLT."
    )
    p.add_argument("--alto-dir",  default=str(repo_dir / "alto"),         help="Directory with ALTO XML files")
    p.add_argument("--ocr-dir",   default=str(repo_dir / "ocr"),          help="Output directory for JSON files")
    p.add_argument("--xsl",       default=str(script_dir / "transform.xsl"), help="XSLT stylesheet")
    p.add_argument("--base-uri",  default=None,                            help="Override baseURI parameter in XSL")
    p.add_argument("--x-ratio",   default=None, type=float,               help="Override xRatio parameter in XSL")
    p.add_argument("--y-ratio",   default=None, type=float,               help="Override yRatio parameter in XSL")
    p.add_argument("--pattern",   default="HKW_M34_*.xml",                help="Glob pattern for ALTO files")
    p.add_argument("--dry-run",   action="store_true",                    help="Transform but do not write files")
    return p.parse_args()


def extract_sequence_nr(stem: str) -> int:
    """Extract the trailing numeric sequence number from a filename stem.

    e.g. 'HKW_M34_0139'              -> 139
         'EHC_e772_2025_0011'         -> 11
         'EHC_B40593_..._MF_0001.alto' -> 1  (strips trailing .alto before splitting)
    """
    # strip a trailing .alto segment that survives Path.stem when extension is .xml
    clean = stem
    if clean.endswith(".alto"):
        clean = clean[:-5]
    return int(clean.split("_")[-1])


def main():
    args = parse_args()

    alto_dir = Path(args.alto_dir)
    ocr_dir  = Path(args.ocr_dir)
    xsl_path = Path(args.xsl)

    # Validate inputs
    if not alto_dir.is_dir():
        sys.exit(f"ALTO directory not found: {alto_dir}")
    if not xsl_path.is_file():
        sys.exit(f"XSL file not found: {xsl_path}")

    # Load and compile stylesheet
    print(f"Loading stylesheet: {xsl_path}")
    xsl_doc = etree.parse(str(xsl_path))
    transform = etree.XSLT(xsl_doc)

    # Collect and sort ALTO files by sequence number
    alto_files = sorted(
        alto_dir.glob(args.pattern),
        key=lambda p: extract_sequence_nr(p.stem)
    )
    if not alto_files:
        sys.exit(f"No ALTO files found in {alto_dir} matching '{args.pattern}'")
    print(f"Found {len(alto_files)} ALTO files")

    # Create output directory
    if not args.dry_run:
        ocr_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {ocr_dir}")

    # Build XSLT parameter overrides
    xslt_params = {}
    if args.base_uri is not None:
        xslt_params["baseURI"] = f"'{args.base_uri}'"
    if args.x_ratio is not None:
        xslt_params["xRatio"] = str(args.x_ratio)
    if args.y_ratio is not None:
        xslt_params["yRatio"] = str(args.y_ratio)

    # Transform each file
    errors = []
    written = 0
    for alto_file in alto_files:
        nr = extract_sequence_nr(alto_file.stem)
        out_file = ocr_dir / f"page-{nr}.json"

        try:
            doc = etree.parse(str(alto_file))
            result = transform(
                doc,
                **{"source-file": f"'{alto_file.name}'", "pageNr": f"'{nr}'"},
                **xslt_params
            )

            # Validate JSON output
            output = str(result)
            json.loads(output)  # raises if invalid

            if not args.dry_run:
                out_file.write_text(output, encoding="utf-8")
                written += 1
            else:
                print(f"  [dry-run] would write {out_file.name}")

        except json.JSONDecodeError as e:
            errors.append((alto_file.name, f"Invalid JSON output: {e}"))
        except Exception as e:
            errors.append((alto_file.name, str(e)))

    # Report
    print(f"\nDone: {written} file(s) written, {len(errors)} error(s)")
    if errors:
        print("Errors:")
        for name, msg in errors:
            print(f"  {name}: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
