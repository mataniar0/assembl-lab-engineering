# MEB-000 reproducible reference verification

Use the existing isolated checkout; do not create a worktree. Python3.12 is tested.
From repository root:

```sh
python -m venv /workspace/.venvs/meb-000
/workspace/.venvs/meb-000/bin/pip install -r projects/MEB-01/tools/requirements.lock
```

Pinned direct dependencies are in requirements.txt; the tested transitive versions
are in requirements.lock. No credentials, native CAD engine or server is needed.
GitHub read uses the existing HTTPS Git proxy. For a fresh external source copy:

```sh
git clone --no-checkout https://github.com/mataniar0/assembl-lab-site.git /tmp/meb-legacy-site
git -C /tmp/meb-legacy-site checkout --detach ebeefe308efaf80329e16e42a84d51557878fd58
```

If that path exists, preserve it; first verify its HEAD, status and registered
blobs rather than resetting or replacing an existing checkout. Source originals
must not be changed. All20registered blobs are compared with Git objects and the
inventory before any geometry calculation.

```sh
python projects/MEB-01/specifications/MEB-000/validate_intake.py --self-test
/workspace/.venvs/meb-000/bin/python -m unittest discover -s projects/MEB-01/tests -v
/workspace/.venvs/meb-000/bin/python projects/MEB-01/tools/audit_geometry.py --source /tmp/meb-legacy-site --output /tmp/meb-geometry-recheck.json --profiles /tmp/meb-profiles-recheck.json
python projects/MEB-01/reports/MEB-000-independent-raw-qa.py /tmp/meb-legacy-site
/workspace/.venvs/meb-000/bin/python projects/MEB-01/tools/reconstruct_reference.py --output projects/MEB-01/proposals/G0-reference/generated
```

The geometry command **currently exits1** because the existing6mm layout fails
owner-approved800H×440W stock. The JSON separately records provenance, file
geometry,49scopedPASS/7NOT_RUN historical-index mapping and target packing
PASS/FAIL. Preserve that exit code in logs; do not describe the entire command as
passing. A parser, provenance or unexpected assertion failure also needs diagnosis.
The4mm bounds check passes. Neither result is a production release.

The independent script's primary63cases use only the Python standard library.
DXF/SVG generation is deterministic in geometry; ezdxf may change timestamps/GUIDs.
Compare model geometry, not generated whole-file SHA across reruns.
No service process needs restarting. Full solid motion, bent-tab containment,
physical measurements and a generative design kernel are outside this G0 reference
verification. G0/datum review and MEB-B12 thin-web assessment are still required.
