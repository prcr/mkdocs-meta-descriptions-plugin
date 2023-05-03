# mkdocs-meta-descriptions-plugin

[![CI/CD](https://github.com/prcr/mkdocs-meta-descriptions-plugin/actions/workflows/test-build-deploy.yml/badge.svg)](https://github.com/prcr/mkdocs-meta-descriptions-plugin/actions/workflows/test-build-deploy.yml)
[![Codacy](https://app.codacy.com/project/badge/Grade/08bc759a053f475091318f53ea67bd05)](https://www.codacy.com/gh/prcr/mkdocs-meta-descriptions-plugin/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=prcr/mkdocs-meta-descriptions-plugin&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/08bc759a053f475091318f53ea67bd05)](https://www.codacy.com/gh/prcr/mkdocs-meta-descriptions-plugin/dashboard?utm_source=github.com&utm_medium=referral&utm_content=prcr/mkdocs-meta-descriptions-plugin&utm_campaign=Badge_Coverage)
[![PyPI](https://img.shields.io/pypi/dm/mkdocs-meta-descriptions-plugin?label=PyPI)](https://pypi.org/project/mkdocs-meta-descriptions-plugin/)

Use this MkDocs plugin to automatically generate meta descriptions for your pages using the first paragraph of each page. This is useful if you start each page with a short introduction or summary that can be reused as the meta description.

![Meta description obtained from first paragraph of the page](https://raw.githubusercontent.com/prcr/mkdocs-meta-descriptions-plugin/main/images/readme-example.png)

For each page, the plugin:

1.  Checks that the page doesn't already have a meta description.

    The plugin **doesn't change** any meta descriptions defined explicitly on the [page meta-data](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data).

2.  Tries to find the first paragraph above any `<h2>` to `<h6>` headings.

    The plugin only searches for the first paragraph until the start of the first section to ensure that the content is from the "introductory" part of the page.

3.  Sets the meta description of the page to the plain text context of the paragraph, stripped of HTML tags.

If the page doesn't have a meta description defined manually by you nor automatically by the plugin, MkDocs sets the meta description of the page to the value of your [`site_description`](https://www.mkdocs.org/user-guide/configuration/#site_description) as a fallback.

## Setting up and using the plugin

> ⚠️ **Important:** to use this plugin, you must either [customize your existing theme](https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks) to include the value of [`page.meta.description`](https://www.mkdocs.org/user-guide/custom-themes/#pagemeta) in the HTML element `<meta name="description" content="...">`, or use an [MkDocs theme](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes) that already does this by default. I recommend using the excellent [Material theme](https://github.com/squidfunk/mkdocs-material).

To set up and use the plugin:

1.  Install the plugin using pip:

    ```bash
    pip install mkdocs-meta-descriptions-plugin
    ```

    Depending on your project, you may also need to add the plugin as a dependency on your `requirements.txt` file.

2.  Activate the plugin in your `mkdocs.yml`:

    ```yaml
    plugins:
      - search
      - meta-descriptions
    ```

    > **Note:** If you have no `plugins` entry in your `mkdocs.yml` file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

## Configuring the plugin

Use the following options to configure the behavior of the plugin:

```yaml
plugins:
  - meta-descriptions:
      export_csv: false
      quiet: false
      enable_checks: false
      min_length: 50
      max_length: 160
```

### `export_csv`

If `true`, the plugin exports the meta descriptions of all Markdown pages to the CSV file `<site_dir>/meta-descriptions.csv`. The default is `false`.

This is useful to review and keep track of all the meta descriptions for your pages, especially if you're maintaining a big site.

### `quiet`

If `true`, the plugin logs messages of level `INFO` using the level `DEBUG` instead. The default is `false`.

Enable this option to have a cleaner MkDocs console output. You can still see all logs by running MkDocs with the `--verbose` flag.

### `enable_checks`

If `true`, the plugin outputs a warning for each page that will have an empty or default meta description, as well as for each meta description shorter than `min_length` or longer than `max_length`. The default is `false`.

Enable this option if you want to make sure that all pages have a meta description and that each meta description follows general SEO best practices.

### `min_length`

Minimum number of characters that each meta description should have. The default is 50 characters, based on [these general recommendations](https://moz.com/learn/seo/meta-description).

Make sure that you set `enable_checks: true` for this option to have an effect.

### `max_length`

Maximum number of characters that each meta description should have. The default is 160 characters, based on [these general recommendations](https://moz.com/learn/seo/meta-description).

Make sure that you set `enable_checks: true` for this option to have an effect.

## See also

Read more about [using MkDocs plugins](http://www.mkdocs.org/user-guide/plugins/).
