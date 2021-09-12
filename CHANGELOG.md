# Change log

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
