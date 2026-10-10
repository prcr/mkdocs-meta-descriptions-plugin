# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An MkDocs plugin (`meta-descriptions`, published on PyPI as `mkdocs-meta-descriptions-plugin`) that sets `page.meta["description"]` from the first paragraph of each page when the page has no explicit description in its front matter. The theme is responsible for rendering it as `<meta name="description">`.

## Commands

```bash
# Install the plugin in editable mode plus test dependencies
pip install -r tests/requirements.txt

# Run all tests with coverage (must run from the repo root, see below)
pytest --cov

# Run one test class / one test
pytest tests/test_plugin.py::TestTrim
pytest tests/test_plugin.py::TestTrim::test_trim_long_first_paragraph

# Run everything against a single MkDocs config and URL mode
pytest -k "mkdocs-trim-default.yml and no-directory-urls"

# Build the test site by hand to inspect the output
mkdocs build --config-file tests/mkdocs.yml --site-dir /tmp/site --verbose

# Build the sdist and wheel (needs full git history and tags for the version)
python -m build --sdist --wheel --outdir dist/ .
```

There is no linter for Python code. Markdown files follow `.markdownlint.json` (4-space list indentation, `-` bullets, `1.` for every ordered item, 3 spaces after a bullet marker and 2 after an ordered marker).

## Architecture

The package `mkdocs_meta_descriptions_plugin` has four small modules:

-   `plugin.py`: `MetaDescription(BasePlugin)`, registered through the `mkdocs.plugins` entry point in `setup.py`. Flow across MkDocs events:
    -   `on_config` initializes the `logger` and `checker` singletons from the plugin config.
    -   `on_page_content` skips pages with a front matter description; otherwise it cuts the rendered HTML at the first `<h2>`–`<h6>`, takes the first `<p>` that isn't directly inside `div.admonition`, and stores its HTML-escaped text in `page.meta["description"]`, applying `trim` and `fallback_if_short`. Leaving the description unset is what makes the theme fall back to `site_description`.
    -   `on_post_page` runs the length checks and collects pages for the export.
    -   `on_post_build` logs the summary and writes the CSV.
-   `common.py`: the `logger` singleton. It branches on the MkDocs version: `get_plugin_logger` for MkDocs 1.5.0 or later, and a plain `logging` logger with a `[meta-descriptions] ` prefix before that. `quiet` downgrades `INFO` messages to `DEBUG`.
-   `checker.py`: the `checker` singleton that emits the `enable_checks` warnings for missing, too short, or too long descriptions.
-   `export.py`: `Export` reads the meta descriptions back from the **generated HTML files** in `site_dir`, not from `page.meta`, so the CSV reflects what the theme actually rendered, including the `site_description` fallback.

Adding or changing a plugin option touches several places: `config_scheme` in `plugin.py`, `schema.json` (JSON schema used by editors for `mkdocs.yml` validation), the options section of `README.md`, and `CHANGELOG.md`.

Option interactions that are easy to miss:

-   None of the options ever change a description that comes from the page front matter. `trim` and `fallback_if_short` only apply to first-paragraph descriptions; `enable_checks` still warns about front matter descriptions.
-   `min_length` is used by both `enable_checks` and `fallback_if_short`; `max_length` is used by both `enable_checks` and `trim`.

## README.md

`README.md` is the only user documentation, and `setup.py` also publishes it as the PyPI long description. Because of that, images must use absolute `raw.githubusercontent.com` URLs, not relative paths.

Its structure is: what the plugin does for each page (a 3-step list that must stay in sync with `on_page_content`), a setup section, and a "Configuring the plugin" section with a YAML block listing **every option with its default**, followed by one `` ### `option_name` `` heading per option in the same order.

-   Each option section starts with "If `true`, the plugin …. The default is `false`." (or the equivalent for numeric options), then says when the option is useful and which other options it depends on.
-   The option headings are link targets: `schema.json` and `CHANGELOG.md` link to `README.md#option_name`. Renaming a heading breaks those links.

## CHANGELOG.md

`CHANGELOG.md` follows Keep a Changelog and Semantic Versioning, and only lists changes that are visible to users of the plugin. Dependency bumps, CI and tooling changes are left out.

-   There is no "Unreleased" section. Each release has a heading in the form `## [vX.Y.Z](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/vPREVIOUS...vX.Y.Z) (YYYY-MM-DD)`, newest first, with `### Added`, `### Changed`, `### Removed` and `### Fixed` subsections as needed.
-   The version in the heading must match the git tag that is pushed for the release, since the tag is what sets the package version.
-   Versioning as practiced so far: dropping a Python version is a major release, a new option or a newly supported Python version is a minor release, and bug fixes are patch releases.
-   Entries for options link to the README anchor, entries for issues end with "Fixes [#N](issue URL).", and outside contributors are thanked by GitHub handle.

## Tests

`tests/test_plugin.py` is integration-only: a module-scoped `build` fixture runs a real `mkdocs build` through Click's `CliRunner` for **every `tests/*.yml` file**, each with both `--use-directory-urls` and `--no-directory-urls`, against the pages in `tests/docs/`. Every test then runs once per combination.

-   Tests decide what to assert by **substring-matching the config file name**, for example `if "fallback-if-short" in mkdocs_yml` or `mkdocs_yml.endswith("mkdocs-export-csv.yml")`. A new `tests/mkdocs-*.yml` file is picked up automatically, and its name determines which existing assertions apply to it, so choose names carefully.
-   Tests that don't match the current config pass without asserting anything.
-   Paths such as `tests/*.yml` and `tests/docs/` are relative to the working directory, so run pytest from the repo root.
-   CSV export tests compare byte-for-byte against the fixtures `tests/meta-descriptions*.csv`, with a `-no-directory-urls` variant of each. Adding a page to `tests/docs/` requires updating all of these fixtures.
-   Checker tests assert on exact log lines in `result.stderr`, with separate expected strings for MkDocs before and after 1.5.0.
-   `tests/mkdocs.yml` is also the config that CI uses to deploy the demo site to GitHub Pages.

## Release and CI

`.github/workflows/test-build-deploy.yml` runs on every push: tests on Python 3.10 to 3.14, coverage to Coveralls, then a build. Pushes to `main` publish to Test PyPI and deploy GitHub Pages; pushing a tag also publishes to PyPI.

The package version comes from git tags through `setuptools_scm`; there is no version string in the source. When supported Python versions change, update both the CI matrix and the classifiers in `setup.py`. Runtime dependencies live in the root `requirements.txt`, which `setup.py` reads as `install_requires`.

Pushing a `vX.Y.Z` tag is the release and can't be undone on PyPI, so never create or push tags without being asked. `.claude/settings.json` pre-approves the routine git, gh, pytest, pip and mkdocs commands, but keeps force pushes and tag pushes behind a confirmation prompt.
