"""Validate and package only public release inputs (no local config or run data)."""
import argparse
import ast
import hashlib
from pathlib import Path
import re
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
TOP = {"README.md", "CLAUDE.md", "LICENSE", "NOTICE.md", "CONTRIBUTORS.md",
       "CONTRIBUTING.md", "CHANGELOG.md", "VERSION", ".gitignore"}


def release_files():
    result = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if "__pycache__" in rel.parts or p.suffix == ".pyc":
            continue
        allowed = (rel.as_posix() in TOP or rel.as_posix() == "config/run.example.json"
                   or rel.parts[0] in {"docs", "tools"}
                   or rel.parts[:2] == (".github", "workflows")
                   or rel.parts[:2] == (".claude", "skills"))
        if allowed:
            if p.is_symlink():
                raise ValueError(f"Symlinks are not release inputs: {rel}")
            if any(part in {".local", ".git", "workspaces", "worktrees"} for part in rel.parts) or ".local." in p.name:
                raise ValueError(f"Private file in release tree: {rel}")
            result.append(p)
    return sorted(result)


def check():
    files = release_files()
    skill_files = list((ROOT / ".claude/skills").glob("*/SKILL.md"))
    if len(skill_files) != 11:
        raise ValueError("Expected coordinator and ten step skills")
    for p in skill_files:
        text = p.read_text(encoding="utf-8-sig")
        match = re.match(r"---\s*\nname: ([a-z0-9-]+)\n", text)
        if not match or match[1] != p.parent.name or "description:" not in text.split("---", 2)[1]:
            raise ValueError(f"Invalid skill frontmatter: {p.name}")
    for p in files:
        if p.suffix == ".py":
            ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        if p.suffix in {".md", ".py", ".json", ".html", ".yml"}:
            text = p.read_text(encoding="utf-8-sig")
            # Reject actual private network addresses, personal Windows paths and student IDs.
            patterns = [r"(?<![\d.])192\.168\.\d+\.\d+", r"(?<![\d.])10\.\d+\.\d+\.\d+",
                        r"(?i)[A-Z]:\\Users\\(?!<)[^\s\\`]+", r"(?i)\bb\d{2}dcat\d{3}\b",
                        r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"]
            for pattern in patterns:
                if re.search(pattern, text):
                    raise ValueError(f"Private-value pattern in {p.relative_to(ROOT)}")
            if p.suffix == ".md":
                for link in re.findall(r"\]\(([^)]+)\)", text):
                    if "://" in link or link.startswith("#"):
                        continue
                    if not (p.parent / link.split("#")[0]).exists():
                        raise ValueError(f"Broken link in {p.relative_to(ROOT)}: {link}")
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "build"])
    args = parser.parse_args()
    try:
        files = check()
        print(f"Validated 11 skills and {len(files)} release files.")
        if args.action == "build":
            version = (ROOT / "VERSION").read_text().strip()
            out = ROOT / "dist" / f"labtainer-spec-{version}.zip"
            out.parent.mkdir(exist_ok=True)
            with ZipFile(out, "w", ZIP_DEFLATED) as archive:
                for p in files:
                    archive.write(p, Path("labtainer-spec") / p.relative_to(ROOT))
            with ZipFile(out) as archive:
                if archive.testzip() is not None:
                    raise ValueError("Archive CRC verification failed")
            digest = hashlib.sha256(out.read_bytes()).hexdigest()
            out.with_suffix(".zip.sha256").write_text(f"{digest}  {out.name}\n", encoding="ascii")
            print(f"Built {out.name}; SHA-256 written alongside it.")
    except (ValueError, OSError, SyntaxError) as exc:
        parser.exit(1, f"Release check failed: {exc}\n")


if __name__ == "__main__":
    main()
