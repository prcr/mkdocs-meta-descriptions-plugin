---
name: update-changelog
description: Add the entry for a new release to CHANGELOG.md, covering every user-facing change since the last release tag and bumping the version according to semver. Use when asked to prepare a release, update the changelog, or write release notes for this plugin.
argument-hint: "[version]"
---

# Update the changelog for a new release

Add one new release entry to the top of `CHANGELOG.md`. The entry must cover every user-facing change since the last release and carry the next version number according to Semantic Versioning.

If the user passed a version as an argument (`$ARGUMENTS`), use it instead of working one out in step 4, but say so if it disagrees with what the changes call for.

## 1. Find the last release

```bash
git fetch --tags
git describe --tags --abbrev=0
```

The result is the previous version (`vPREVIOUS`). Check that it matches the topmost heading in `CHANGELOG.md`. If the changelog already has an entry for a version that has no tag yet, update that entry instead of adding a second one.

## 2. Collect the changes since that release

```bash
git log vPREVIOUS..HEAD --no-merges --oneline
git diff vPREVIOUS..HEAD --stat
```

Don't rely on commit subjects alone: prefixes in this repository are inconsistent and some user-facing commits have none. Read the diff of everything that can affect users:

```bash
git diff vPREVIOUS..HEAD -- mkdocs_meta_descriptions_plugin/ setup.py requirements.txt schema.json README.md
```

For commits that reference a pull request or issue (`(#123)`), run `gh pr view 123` to get the motivation, the linked issue and the author to credit.

## 3. Decide what is user-facing

Include a change only if someone who installs and uses the plugin can notice it:

| Include | Section |
| --- | --- |
| New plugin option, new log message, new capability | `### Added` |
| Newly supported Python version (new classifier in `setup.py` and new entry in the CI matrix) | `### Added` |
| Different behavior of an existing option, different output or log format, different default | `### Changed` |
| Dropped Python version, removed option or behavior | `### Removed` |
| Bug fix in the plugin or in its packaging | `### Fixed` |

Leave out everything else: Dependabot bumps of `tests/requirements.txt` and GitHub Actions, CI and workflow changes (`toolchain:`), test-only changes, refactors with no behavior change, funding and repository metadata, `CLAUDE.md` and `.claude/`, and README edits that only reword existing documentation.

A raised minimum version in the root `requirements.txt` changes what users must have installed. Past releases haven't listed these, so don't add them silently: point them out to the user and ask whether to include them.

If nothing is user-facing, stop and tell the user that there is nothing to release. Don't write an empty entry.

## 4. Work out the new version

Apply the highest bump that any included change calls for:

-   **Major**: anything under `### Removed`, including a dropped Python version, or a `### Changed` item that can break an existing setup.
-   **Minor**: anything under `### Added`, or a backward-compatible `### Changed` item.
-   **Patch**: only `### Fixed` items.

## 5. Write the entry

Insert the entry directly above the previous release, below the introduction of the file. Use today's date.

```markdown
## [vX.Y.Z](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/vPREVIOUS...vX.Y.Z) (YYYY-MM-DD)

### Added

-   New option [`option_name`](https://github.com/prcr/mkdocs-meta-descriptions-plugin#option_name) to do something for the user. Fixes [#123](https://github.com/prcr/mkdocs-meta-descriptions-plugin/issues/123). Thanks to [@handle](https://github.com/handle) for the contribution! 🎉
-   Added support for [Python 3.NN](https://www.python.org/downloads/release/python-3NN0/).

### Removed

-   Dropped support for Python 3.N after [reaching EOL on YYYY-MM-DD](https://devguide.python.org/versions/#unsupported-versions).
```

Rules for the entry:

-   Only add the subsections that have items, in the order Added, Changed, Removed, Fixed.
-   Write each item for users of the plugin: say what they can now do or what changed for them, not how the code changed.
-   Link each option to its README anchor, and check that the `` ### `option_name` `` heading exists in `README.md`.
-   End items that close an issue with "Fixes [#N](issue URL)." and thank outside contributors (anyone other than the repository owner) by GitHub handle, saying whether it was an idea or a contribution.
-   Look up the real Python release link and the real end-of-life date. Don't guess them.
-   Follow `.markdownlint.json`: `-` bullets followed by 3 spaces, one blank line around headings and lists.

Read existing entries in `CHANGELOG.md` for the tone and wording to match.

## 6. Report back

Tell the user the new version, the bump type and the reason for it, the items you included, and any commits you left out that they might consider user-facing.

Stop there. Don't create or push the `vX.Y.Z` tag: pushing it publishes the release to PyPI, which can't be undone, so that step is the user's.
