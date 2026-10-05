"""Check packaging and obvious disclosure patterns; not a confidentiality guarantee."""
import pathlib
import json
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve()
private_terms = json.loads(pathlib.Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 and sys.argv[2] else []
if not isinstance(private_terms, list) or any(not isinstance(term, str) or not term for term in private_terms):
    raise SystemExit("Private term file must contain a JSON list of nonempty strings.")
patterns = [
    r"/(?:Users|home)/[^/\s]+/",
    r"sk-[A-Za-z0-9_-]{20,}", r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}", r"AKIA[0-9A-Z]{16}",
    r"@[A-Za-z0-9_]{3,}",
]
errors = []
for path in sorted(root.rglob("*")):
    if ".git" in path.parts:
        continue
    if path.is_symlink():
        errors.append(f"symlink: {path.relative_to(root)}")
        continue
    if not path.is_file():
        continue
    if path.name == ".DS_Store" or ".bak" in path.name:
        errors.append(f"unwanted file: {path.relative_to(root)}")
    text = path.read_text()
    # Only this checker's literal patterns are excluded from its generic scan.
    if path.resolve() != pathlib.Path(__file__).resolve():
        if any(re.search(p, text, re.I) for p in patterns):
            errors.append(f"disclosure pattern: {path.relative_to(root)}")
    if any(term.casefold() in text.casefold() for term in private_terms):
        errors.append(f"private term: {path.relative_to(root)}")
    if path.suffix == ".md":
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                errors.append(f"broken link: {path.relative_to(root)} -> {target}")
skill = root / "skills/meeting-notes/SKILL.md"
if not skill.exists():
    errors.append("missing skill")
else:
    text = skill.read_text()
    if not text.startswith("---\nname: meeting-notes\ndescription:"):
        errors.append("invalid skill header")
    if "references/" in text:
        errors.append("unexpected external skill reference")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("PASS: package links, skill header and disclosure-pattern scan")
