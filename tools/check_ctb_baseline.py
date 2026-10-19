"""Repository-level import consistency checks; no CAD or physical validation."""
import csv
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'projects/CTB-01/specifications/CTB-000'
REPORTS = ROOT / 'projects/CTB-01/reports'


def load(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'))


def rows(name):
    with (BASE / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    manifest = load('MANIFEST.json')
    params = load('CTB-000_parameters.json')
    interfaces = load('CTB-000_interfaces.json')
    parts = rows('CTB-000_parts.csv')
    issues = rows('CTB-000_open_issues.csv')
    hashes = json.loads((REPORTS / 'CTB-000-source-sha256.json').read_text())
    Draft202012Validator.check_schema(load('CTB-000_schema.json'))
    Draft202012Validator(load('CTB-000_schema.json')).validate(params)
    checks = {
        'manifest_inventory_15': len(manifest['files']) == 15
        and set(manifest['files']) == {p.name for p in BASE.iterdir() if p.is_file()},
        'source_bytes_unchanged': set(hashes) == set(manifest['files']) and all(
            hashlib.sha256((BASE / name).read_bytes()).hexdigest() == digest
            for name, digest in hashes.items()),
        'parameter_schema': True,
        'baseline_versions': params['version'] == interfaces['version'] == manifest['version'] == 'v0.2',
        'interface_inventory_14': len(interfaces['interfaces']) == 14
        and {i['id'] for i in interfaces['interfaces']} == {f'IF-{n:02}' for n in range(1, 15)},
        'open_issue_inventory_13': len(issues) == 13
        and {i['issue_id'] for i in issues} == {f'B{n:02}' for n in range(1, 14)},
        'critical_blockers_retained': all(next(i for i in issues if i['issue_id'] == key)['severity'] == 'BLOCKER'
                                          for key in ('B01', 'B02', 'B03')),
        'interface_party_references': all(p in {r['part_family_id'] for r in parts} | {'FLOOR'}
                                          for i in interfaces['interfaces'] for p in i['parties']),
        'all_parts_referenced': {r['part_family_id'] for r in parts} <=
                                {p for i in interfaces['interfaces'] for p in i['parties']},
        'no_interface_approval_upgrade': all(i['status'] in {'PROVISIONAL', 'OPEN', 'EXPERIMENTAL'}
                                            for i in interfaces['interfaces']),
        'portrait_sheet': params['frozen']['stock_sheet_height_mm'] == 800
        and params['frozen']['stock_sheet_width_mm'] == 440
        and params['frozen']['stock_sheet_mm'] == [800, 440]
        and params['frozen']['stock_sheet_array_order'] == '[height_mm,width_mm]'
        and params['frozen']['stock_sheet_orientation'] == 'portrait_height_800_width_440',
        'no_active_900_numeric_setting': not any(
            value == 900 for group in ('frozen', 'derived', 'provisional')
            for value in numeric_values(params[group])),
        'svg_parseable': ET.parse(BASE / 'CTB-000_interface_diagram.svg').getroot().tag.endswith('svg'),
        'png_signature': (BASE / 'CTB-000_interface_diagram.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),
        'no_legacy_cad_import': not any(p.suffix.lower() in {'.dxf', '.step', '.stp', '.stl', '.f3d'}
                                      for p in BASE.iterdir()),
    }
    for name, passed in checks.items():
        print(f'{"PASS" if passed else "FAIL"} {name}')
    print(f'Summary: {sum(checks.values())} / {len(checks)} import checks passed')
    return 0 if all(checks.values()) else 1


def numeric_values(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from numeric_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from numeric_values(child)
    elif isinstance(value, (int, float)):
        yield value


if __name__ == '__main__':
    raise SystemExit(main())
