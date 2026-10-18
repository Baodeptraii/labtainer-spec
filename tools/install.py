"""Install all bundled skills into a Claude Code project; never overwrite conflicts."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def install(target):
    target = Path(target).expanduser().resolve()
    source = ROOT / ".claude/skills"
    destination = target / ".claude/skills"
    if destination == source:
        return 0
    files = [(p, destination / p.relative_to(source)) for p in source.rglob("*")
             if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    for src, dst in files:
        if dst.exists() and (not dst.is_file() or dst.read_bytes() != src.read_bytes()):
            raise ValueError(f"Existing file differs; no files installed: {dst}")
    for src, dst in files:
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    config = target / "config/run.example.json"
    if not config.exists():
        config.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "config/run.example.json", config)
    return len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Existing/new Claude project directory")
    args = parser.parse_args()
    try:
        count = install(args.target)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Install failed: {exc}\n")
    print(f"Installed/verified {count} skill files. Restart Claude Code in the target project.")
    print("Existing CLAUDE.md, settings and local credentials were not changed.")


if __name__ == "__main__":
    main()
