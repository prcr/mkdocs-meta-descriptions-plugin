# Change log

This file lists all updates to the [mkdocs-meta-descriptions plugin](https://github.com/prcr/mkdocs-meta-descriptions-plugin).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.2.0](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v2.1.0...v2.2.0) (2022-12-15)

### Added

-   Added support for [Python 3.11](https://www.python.org/downloads/release/python-3111/).

## [v2.1.0](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v2.0.0...v2.1.0) (2022-10-01)

### Added

-   New option [`enable_checks`](https://github.com/prcr/mkdocs-meta-descriptions-plugin#enable_checks) to validate if all pages have meta descriptions and if each meta description has the recommended length.

## [v2.0.0](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v1.0.2...v2.0.0) (2022-07-23)

### Removed

-   Dropped support for Python 3.6 after [reaching EOL on 2021-12-23](https://devguide.python.org/versions/#unsupported-versions).

### Added

-   Added support for [Python 3.10](https://www.python.org/downloads/release/python-3101/).
-   New option [`quiet`](https://github.com/prcr/mkdocs-meta-descriptions-plugin#quiet) to stop info messages from being displayed on the console when running MkDocs.
-   New debug messages to log which meta description the plugin used on each page, available by running MkDocs with the `--verbose` flag.

### Changed

-   Tweaked existing console log messages.

## [v1.0.2](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v1.0.1...v1.0.2) (2021-09-12)

### Fixed

-   Ignore first paragraphs if they belong to an [Admonition card](https://python-markdown.github.io/extensions/admonition/). Fixes [#95](https://github.com/prcr/mkdocs-meta-descriptions-plugin/issues/95).

## [v1.0.1](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v1.0.0...v1.0.1) (2021-05-16)

### Fixed

-   Write full page URLs in `meta-descriptions.csv` if `site_url` is defined. Fixes [#68](https://github.com/prcr/mkdocs-meta-descriptions-plugin/issues/68).
-   Drop lxml dependency by using Python's built-in html.parser instead

## [v1.0.0](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v0.0.5...v1.0.0) (2021-05-15)

First stable version.

### Added

-   Support for [exporting meta descriptions](README.md#export_csv) as CSV file.

## [v0.0.5](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v0.0.4...v0.0.5) (2021-05-10)

### Fixed

-   Slacken minimum requirements for Python packages to make the plugin compatible with a wider range of environments.

## [v0.0.4](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v0.0.3...v0.0.4) (2021-04-27)

### Fixed

-   Correct package name in setup.py that was preventing the plugin from being used in MkDocs.

## [v0.0.3](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v0.0.2...v0.0.3) (2021-04-24)

### Fixed

-   Escape special characters `& < " ' >` in text used in meta descriptions. Fixes [#35](https://github.com/prcr/mkdocs-meta-descriptions-plugin/issues/35).

## [v0.0.2](https://www.github.com/prcr/mkdocs-meta-descriptions-plugin/compare/v0.0.1...v0.0.2) (2021-04-06)

First working version with documentation.
