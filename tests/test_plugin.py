import filecmp
import glob
import os.path
import tempfile

import pytest
from bs4 import BeautifulSoup
from click.testing import CliRunner
from mkdocs.__main__ import build_command
from mkdocs.structure.files import File, Files

mkdocs_yml_list = glob.glob("tests/*.yml")
markdown_files_list = [
    file[len("tests/docs/") :]
    for file in glob.glob("tests/docs/**/*.md", recursive=True)
]


def get_meta_description(files, markdown_file_path):
    html_file_path = files.get_file_from_path(markdown_file_path).abs_dest_path
    with open(html_file_path) as file:
        html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        result = soup.select_one('meta[name="description"]')
        return result["content"] if result else None


@pytest.fixture(
    scope="module",
    params=[True, False],
    ids=["use-directory-urls", "no-directory-urls"],
)
def use_directory_urls(request):
    flag = "--use-directory-urls" if request.param else "--no-directory-urls"
    return flag, request.param


@pytest.fixture(scope="module", params=mkdocs_yml_list)
def build(request, use_directory_urls):
    mkdocs_yml = request.param
    with tempfile.TemporaryDirectory() as tempdir:
        result = CliRunner(mix_stderr=False).invoke(
            build_command,
            ["--config-file", mkdocs_yml, "--site-dir", tempdir, use_directory_urls[0], "--verbose"],
        )
        files = Files(
            [
                File(
                    file,
                    os.path.join(os.getcwd(), "tests/docs/"),
                    tempdir,
                    use_directory_urls[1],
                )
                for file in markdown_files_list
            ]
        )
        yield result, files, mkdocs_yml, use_directory_urls[1]


class TestPlugin:
    def test_build(self, build):
        result, _, _, _ = build
        assert result.exit_code == 0

    def test_build_output(self, build):
        _, files, _, _ = build
        for f in files:
            assert os.path.isfile(f.abs_dest_path)

    def test_index_md(self, build):
        _, files, _, _ = build
        expected = "For full documentation visit mkdocs.org."
        assert get_meta_description(files, "index.md") == expected

    def test_first_paragraph(self, build):
        _, files, _, _ = build
        expected = "First paragraph."
        assert get_meta_description(files, "first-paragraph.md") == expected

    def test_first_paragraph_no_heading(self, build):
        _, files, _, _ = build
        expected = "First paragraph."
        assert get_meta_description(files, "first-paragraph-no-heading.md") == expected

    def test_first_paragraph_no_paragraph(self, build):
        _, files, mkdocs_yml, _ = build
        if "no-site-description" in mkdocs_yml:
            expected = None
        else:
            expected = "Value of site_description on mkdocs.yml"
        assert (
            get_meta_description(files, "first-paragraph-no-paragraph.md") == expected
        )

    def test_first_paragraph_no_intro(self, build):
        _, files, mkdocs_yml, _ = build
        if "no-site-description" in mkdocs_yml:
            expected = None
        else:
            expected = "Value of site_description on mkdocs.yml"

        assert get_meta_description(files, "first-paragraph-no-intro.md") == expected

    def test_front_matter_description(self, build):
        _, files, _, _ = build
        expected = "Value of meta description on front-matter-description.md"
        assert get_meta_description(files, "front-matter-description.md") == expected

    def test_escape_html_entities(self, build):
        _, files, _, _ = build
        expected = (
            "First paragraph with HTML entities: \"quotes\", 'single quotes', "
            "<greater and less than>, &ampersand&."
        )
        assert get_meta_description(files, "escape-html-entities.md") == expected

    def test_build_summary(self, build):
        result, _, mkdocs_yml, _ = build
        if "quiet" in mkdocs_yml:
            not_expected = "INFO     -  [meta-descriptions]"
            assert not_expected not in result.output


class TestExport:
    def test_export_csv_output(self, build):
        _, files, mkdocs_yml, use_directory_urls = build
        if mkdocs_yml.endswith("mkdocs-export-csv.yml"):
            index_path = files.get_file_from_path("index.md").abs_dest_path
            csv_path = index_path.replace("index.html", "meta-descriptions.csv")
            if use_directory_urls:
                assert filecmp.cmp("tests/meta-descriptions.csv", csv_path)
            else:
                assert filecmp.cmp(
                    "tests/meta-descriptions-no-directory-urls.csv", csv_path
                )

    def test_export_csv_output_no_site_description(self, build):
        _, files, mkdocs_yml, use_directory_urls = build
        if mkdocs_yml.endswith("mkdocs-export-csv-no-site-description.yml"):
            index_path = files.get_file_from_path("index.md").abs_dest_path
            csv_path = index_path.replace("index.html", "meta-descriptions.csv")
            if use_directory_urls:
                assert filecmp.cmp(
                    "tests/meta-descriptions-no-site-description.csv", csv_path
                )
            else:
                assert filecmp.cmp(
                    "tests/meta-descriptions-no-site-description-no-directory-urls.csv",
                    csv_path,
                )

    def test_export_csv_output_no_site_url(self, build):
        _, files, mkdocs_yml, use_directory_urls = build
        if mkdocs_yml.endswith("mkdocs-export-csv-no-site-url.yml"):
            index_path = files.get_file_from_path("index.md").abs_dest_path
            csv_path = index_path.replace("index.html", "meta-descriptions.csv")
            if use_directory_urls:
                assert filecmp.cmp("tests/meta-descriptions-no-site-url.csv", csv_path)
            else:
                assert filecmp.cmp(
                    "tests/meta-descriptions-no-site-url-no-directory-urls.csv",
                    csv_path,
                )


class TestChecker:
    def test_checker_long(self, build):
        result, _, mkdocs_yml, _ = build
        if "enable-checks" in mkdocs_yml:
            expected = "WARNING  -  \x1b[0m[meta-descriptions] Meta description 10 characters longer than 35: " \
                       "warning-long.md"
            assert expected in result.stderr

    def test_checker_short(self, build):
        result, _, mkdocs_yml, _ = build
        if "enable-checks" in mkdocs_yml:
            expected = "WARNING  -  \x1b[0m[meta-descriptions] Meta description 2 characters shorter than 25: " \
                       "warning-short.md"
            assert expected in result.stderr

    def test_checker_not_found(self, build):
        result, _, mkdocs_yml, _ = build
        if "enable-checks" in mkdocs_yml:
            expected = "WARNING  -  \x1b[0m[meta-descriptions] Meta description not found: " \
                       "warning-not-found.md"
            assert expected in result.stderr
