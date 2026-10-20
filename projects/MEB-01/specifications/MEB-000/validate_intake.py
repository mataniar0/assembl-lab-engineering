#!/usr/bin/env python3
"""MEB-000 intake contract/static consistency checks (not geometric or physical QA)."""
import argparse
import csv
import io
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def validate(parts, interfaces, params, inventory, issues):
    errors = []
    def check(cond, msg):
        if not cond:
            errors.append(msg)

    ids = [r["part_id"] for r in parts]
    names = [r["legacy_filename"] for r in parts]
    quantities = [int(r["qty"]) for r in parts]
    check(len(ids) == 14, "Expected 14 distinct part IDs")
    check(len(set(ids)) == len(ids), "Duplicate part ID")
    check(len(set(names)) == 14, "Legacy source filename duplicated")
    check(sum(quantities) == 17, "Expected 17 reported part instances")
    check(all(q > 0 for q in quantities), "Invalid part quantity")
    check(set(r["status"] for r in parts) == {"LEGACY_REPORTED_NOT_CAD_VERIFIED"}, "Part QA labels exceed evidence")
    check(params["release_scope"] == "DESIGN_ONLY_G0_DRAFT", "Forbidden release status")
    pids = [p["id"] for p in params["values"]]
    check(len(pids) == len(set(pids)), "Duplicate parameter")
    check(params["coordinate_system"]["units"] == "mm" and params["coordinate_system"]["angle_units"] == "deg", "Coordinate units mismatch")
    approved_units = {"TARGET_SHEET_HEIGHT": "mm", "TARGET_SHEET_WIDTH": "mm", "OPENING_ANGLE_REQUIRED": "deg"}
    approved = {"TARGET_SHEET_HEIGHT": 800, "TARGET_SHEET_WIDTH": 440, "OPENING_ANGLE_REQUIRED": 110}
    check(all(p["status"] in ("PROVISIONAL", "OPEN", "LEGACY_REPORTED") or
              (p["status"] == "FROZEN" and p["id"] in approved and p["value"] == approved[p["id"]]
               and p["unit"] == approved_units[p["id"]] and p.get("approved_by") == "Product owner" and p.get("approved_date") == "2026-10-20")
              for p in params["values"]), "Unexpected frozen/approved parameter")
    check(all(any(p["id"] == name and p["value"] == value and p["status"] == "FROZEN"
                  for p in params["values"]) for name, value in approved.items()), "Owner requirement mismatch")
    check(all(p["value"] is None for p in params["values"] if p["status"] == "OPEN"), "Open parameter with a nominal value")
    interfaces_list = interfaces["interfaces"]
    ifids = [x["id"] for x in interfaces_list]
    check(len(ifids) == 11 and len(set(ifids)) == 11, "Expected 11 unique interfaces")
    check(all(set(x["parts"]).issubset(set(ids)) for x in interfaces_list), "Interface references undefined part")
    check(all(x["status"] == "OPEN" for x in interfaces_list), "Interface inappropriately claims validation")
    files = inventory["files"]
    paths = [f["path"] for f in files]
    check(len(files) == 20 and len(set(paths)) == 20, "Source inventory count/unique paths mismatch")
    check(SHA40.fullmatch(inventory["source_commit_sha"]) is not None, "Missing pinned source commit")
    check(all(SHA40.fullmatch(f["sha"]) is not None and int(f["size_bytes"]) > 0 for f in files), "Bad source blob sha/size")
    per_part = [f["path"].split("/")[-1] for f in files if f["kind"] == "per_part"]
    check(set(per_part) == set(names), "Part definitions don't match legacy inventory")
    check(sum(f["kind"] == "production" for f in files) == 2, "Expected two legacy nesting sheets")
    check(sum(f["kind"] == "calibration" for f in files) == 1, "Expected one fit coupon")
    issue_ids = [r["id"] for r in issues]
    check(set(issue_ids) == {f"MEB-B{i:02d}" for i in range(1, 13)} and len(issue_ids) == 12, "Expected 12 unique blockers")
    check(all(r["status"] == "OPEN" for r in issues), "Blocker closed without proof")
    return errors


def csv_rows(path):
    with (HERE / path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    parts = csv_rows("PARTS.csv")
    interfaces = json.loads((HERE / "interfaces.json").read_text(encoding="utf-8"))
    params = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    inventory = json.loads((HERE / "LEGACY_SOURCE_INVENTORY.json").read_text(encoding="utf-8"))
    issues = csv_rows("OPEN_ISSUES.csv")
    errors = validate(parts, interfaces, params, inventory, issues)
    if errors:
        for issue in errors:
            print("FAIL", issue)
        raise SystemExit(1)
    print("PASS MEB-000 intake registry consistency (not CAD QA)")
    if args.self_test:
        import copy
        mutants = [
            (parts[:-1], interfaces, params, inventory, issues),
            (parts, {"interfaces": interfaces["interfaces"][:-1]}, params, inventory, issues),
            (parts, interfaces, params, {**inventory, "source_commit_sha": "bad"}, issues),
            (parts, interfaces, params, inventory, issues[:-1])
        ]
        wrong_stock = copy.deepcopy(params)
        next(p for p in wrong_stock["values"] if p["id"] == "TARGET_SHEET_HEIGHT")["value"] = 900
        unapproved_frozen = copy.deepcopy(params)
        next(p for p in unapproved_frozen["values"] if p["id"] == "INNER_LENGTH")["status"] = "FROZEN"
        wrong_angle = copy.deepcopy(params)
        next(p for p in wrong_angle["values"] if p["id"] == "OPENING_ANGLE_REQUIRED")["value"] = 120
        wrong_unit = copy.deepcopy(params)
        next(p for p in wrong_unit["values"] if p["id"] == "TARGET_SHEET_HEIGHT")["unit"] = "inch"
        mutants.append((parts, interfaces, wrong_unit, inventory, issues))
        mutants.extend([(parts, interfaces, wrong_stock, inventory, issues),
                        (parts, interfaces, unapproved_frozen, inventory, issues),
                        (parts, interfaces, wrong_angle, inventory, issues)])
        for i, trial in enumerate(mutants, 1):
            if not validate(*trial):
                print("FAIL negative control", i)
                raise SystemExit(2)
            print("PASS negative control", i, "rejected invalid registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
