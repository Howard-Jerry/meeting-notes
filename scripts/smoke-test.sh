#!/usr/bin/env bash
# Clean-copy check; no installation into the user's agent environment.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$ROOT" <<'PY'
import pathlib, shutil, subprocess, sys, tempfile
root = pathlib.Path(sys.argv[1])
with tempfile.TemporaryDirectory(prefix="meeting-notes-smoke-") as temp:
    clean = pathlib.Path(temp) / "candidate"
    if (root / ".git").exists():
        dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True)
        if dirty.strip():
            raise SystemExit("Commit the reviewed candidate before testing the committed package.")
        subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(root), str(clean)], check=True)
    else:
        shutil.copytree(root, clean, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    subprocess.run(["bash", str(clean / "scripts/guard.sh")], check=True, cwd=temp)
    install = pathlib.Path(temp) / "skills/meeting-notes"
    install.parent.mkdir()
    install.symlink_to(clean / "skills/meeting-notes", target_is_directory=True)
    assert (install / "SKILL.md").read_text().startswith("---")
    for stem in ("01-suggestion", "02-missing-owner", "03-correction", "04-first-use"):
        assert (clean / "examples" / (stem + ".input.md")).is_file()
        assert (clean / "examples" / (stem + ".output.md")).is_file()
    print("PASS: clean package, local skill link and four sample pairs")
PY
