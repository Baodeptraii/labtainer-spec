# Release checklist

## Prepare

1. Update VERSION and CHANGELOG.md. Keep every skill directory name equal to its frontmatter name.
2. Run `python tools/release.py check` and the offline tests in README.
3. Run `python tools/release.py build`. Inspect the ZIP file list and SHA-256.
4. Confirm redistribution permission for the academy template/logo described in NOTICE.md. MIT covers the project code/instructions, not third-party branding.
5. Test a fresh install into a temporary Claude Code project. Do not include that project's config or run artifacts in the release.

## Publish manually

Create your GitHub repository and upload the contents of this release project,
including `.claude/` and `.github/` hidden directories. Do not upload the parent
working directory, credentials, local config or historical lab reports.

Prefer Git from a fresh repository in this release project so the original private
development history is not imported. Review `git status` and staged files before
committing; use the supplied .gitignore. Set your own remote URL, then push.

After GitHub Actions passes, create tag/release `v1.0.0` matching VERSION and attach
the generated ZIP and SHA-256 file. Do not state that CI, remote GUI execution or
every lab passed unless those checks actually ran and their evidence is available.

No GitHub repository URL is embedded in the source until a maintainer supplies the
public destination. README installation from downloaded ZIP works without one.
