# Contributing

Preserve the ordered workflow and operational constraints when editing a skill.
Make the smallest change that addresses a demonstrated issue. Do not replace
detailed step instructions with a summary unless the behavior is intentionally
changed and documented.

1. Change the relevant step skill; update shared references only for shared rules.
2. Keep hostnames, student IDs, credentials, private URLs and execution artifacts out of commits.
3. Run `python tools/release.py check` and the offline tests listed in README.
4. Document behavioral changes in CHANGELOG.md and describe how they were verified.

Tests must use fixtures rather than real credentials or lab evidence. Contributions
to code and instructions are under the project MIT license. Do not submit assets
you cannot redistribute; institutional assets have separate terms in NOTICE.md.
