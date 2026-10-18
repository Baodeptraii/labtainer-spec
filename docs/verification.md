# Verification scope

Run from the repository root:

```sh
python tools/release.py check
python -B -m unittest discover -s .claude/skills/labtainer-spec/tests -v
python tools/release.py build
```

Validation covers eleven skill entrypoints, local links, Python syntax, release allowlist, common private-value patterns, configuration, queue/report invariants, password transport mocks and installation behavior.

Tests are offline fixtures: no VM connection, real screenshots, lab certification or Claude Code integration session. CI is configured for Windows/Linux and Python 3.10/3.12; local success does not establish that remote CI has already run.

The supplied DOCX layout is preserved. Visual rendering and real lab execution remain checks for each actual run. See shared configuration and per-step skills for helper limitations.

Local verification on Windows with Python 3.10: 28 tests passed; all 11 skill
entrypoints passed the UTF-8 skill validator. All original Markdown section
headings were retained in the ten detailed step skills. Known personal values
were checked across public source and embedded DOCX XML. This checks preservation
of structure, not equivalence of agent performance on every lab.

When only skills are installed into another project, the two repository-installer
tests are skipped because tools/install.py belongs to the release repository.
