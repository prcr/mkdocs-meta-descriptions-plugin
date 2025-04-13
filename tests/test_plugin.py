import filecmp
import glob
import os.path
import tempfile

import pytest
from bs4 import BeautifulSoup
from click.testing import CliRunner
from mkdocs.__main__ import build_command
from mkdocs.structure.files import File, Files

from mkdocs_meta_descriptions_plugin.common import MKDOCS_VERSION, MKDOCS_1_5_0

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
        _, files, mkdocs_yml, _ = build
        if "fallback-if-short-default" in mkdocs_yml:
            expected = "Value of site_description on mkdocs.yml"
        else:
            expected = "For full documentation visit mkdocs.org."
        assert get_meta_description(files, "index.md") == expected

    def test_first_paragraph(self, build):
        _, files, mkdocs_yml, _ = build
        if "fallback-if-short" in mkdocs_yml:
            expected = "Value of site_description on mkdocs.yml"
        else:
            expected = "First paragraph."
        assert get_meta_description(files, "first-paragraph.md") == expected

    def test_first_paragraph_no_heading(self, build):
        _, files, mkdocs_yml, _ = build
        if "fallback-if-short" in mkdocs_yml:
            expected = "Value of site_description on mkdocs.yml"
        else:
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
            if MKDOCS_VERSION < MKDOCS_1_5_0:
                not_expected = "INFO     -  [meta-descriptions]"
            else:
                not_expected = "INFO    -  mkdocs_meta_descriptions_plugin"
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

    def test_export_csv_output_trim(self, build):
        _, files, mkdocs_yml, use_directory_urls = build
        if mkdocs_yml.endswith("mkdocs-export-csv-trim.yml"):
            index_path = files.get_file_from_path("index.md").abs_dest_path
            csv_path = index_path.replace("index.html", "meta-descriptions.csv")
            if use_directory_urls:
                assert filecmp.cmp("tests/meta-descriptions-trim.csv", csv_path)
            else:
                assert filecmp.cmp(
                    "tests/meta-descriptions-trim-no-directory-urls.csv", csv_path
                )

    def test_export_csv_output_fallback_if_short(self, build):
        _, files, mkdocs_yml, use_directory_urls = build
        if mkdocs_yml.endswith("mkdocs-export-csv-fallback-if-short.yml"):
            index_path = files.get_file_from_path("index.md").abs_dest_path
            csv_path = index_path.replace("index.html", "meta-descriptions.csv")
            if use_directory_urls:
                assert filecmp.cmp("tests/meta-descriptions-fallback-if-short.csv", csv_path)
            else:
                assert filecmp.cmp(
                    "tests/meta-descriptions-fallback-if-short-no-directory-urls.csv", csv_path
                )


class TestChecker:
    def test_checker_long(self, build):
        result, _, mkdocs_yml, _ = build
        if "enable-checks" in mkdocs_yml:
            if MKDOCS_VERSION < MKDOCS_1_5_0:
                expected = "WARNING  -  \x1b[0m[meta-descriptions] " \
                           "Meta description 10 characters longer than 35: warning-long.md"
            else:
                expected = "WARNING -  \x1b[0mmeta-descriptions: " \
                           "Meta description 10 characters longer than 35: warning-long.md"
            assert expected in result.stderr

    def test_checker_short(self, build):
        result, _, mkdocs_yml, _ = build
        if "enable-checks" in mkdocs_yml:
            if MKDOCS_VERSION < MKDOCS_1_5_0:
                expected = "WARNING  -  \x1b[0m[meta-descriptions] " \
                           "Meta description 2 characters shorter than 25: warning-short.md"
            else:
                expected = "WARNING -  \x1b[0mmeta-descriptions: " \
                           "Meta description 2 characters shorter than 25: warning-short.md"
            assert expected in result.stderr

    def test_checker_not_found(self, build):
        result, _, mkdocs_yml, _ = build
        if "enable-checks" in mkdocs_yml:
            if MKDOCS_VERSION < MKDOCS_1_5_0:
                expected = "WARNING  -  \x1b[0m[meta-descriptions] " \
                           "Meta description not found: warning-not-found.md"
            else:
                expected = "WARNING -  \x1b[0mmeta-descriptions: " \
                           "Meta description not found: warning-not-found.md"
            assert expected in result.stderr


class TestTrim:
    def test_trim_long_description(self, build):
        _, files, mkdocs_yml, _ = build
        if "trim-default" in mkdocs_yml:
            expected = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
                        "labore et dolore magna aliqua. Neque convallis a cras semper auctor neque vitae tempus quam. "
                        "Lacus viverra vitae congue eu consequat ac felis. Amet consectetur adipiscing elit duis "
                        "tristique sollicitudin. Et egestas quis ipsum suspendisse. Donec adipiscing tristique risus "
                        "nec feugiat in fermentum posuere urna. At auctor urna nunc id cursus metus. Risus nec feugiat "
                        "in fermentum posuere urna. Habitant morbi tristique senectus et netus. Diam maecenas "
                        "ultricies mi eget mauris pharetra et ultrices. A arcu cursus vitae congue. Maecenas sed enim "
                        "ut sem viverra aliquet eget sit amet. Placerat vestibulum lectus mauris ultrices eros in.")
            assert get_meta_description(files, "trim-long-description.md") == expected

    def test_trim_long_first_paragraph(self, build):
        _, files, mkdocs_yml, _ = build
        if "trim-default" in mkdocs_yml:
            expected = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
                        "labore et dolore magna aliqua. Neque convallis a cras semper auctor")
            assert get_meta_description(files, "trim-long-first-paragraph.md") == expected

    def test_trim_max_length_long_description(self, build):
        _, files, mkdocs_yml, _ = build
        if "trim-max-length" in mkdocs_yml:
            expected = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
                        "labore et dolore magna aliqua. Neque convallis a cras semper auctor neque vitae tempus quam. "
                        "Lacus viverra vitae congue eu consequat ac felis. Amet consectetur adipiscing elit duis "
                        "tristique sollicitudin. Et egestas quis ipsum suspendisse. Donec adipiscing tristique risus "
                        "nec feugiat in fermentum posuere urna. At auctor urna nunc id cursus metus. Risus nec feugiat "
                        "in fermentum posuere urna. Habitant morbi tristique senectus et netus. Diam maecenas "
                        "ultricies mi eget mauris pharetra et ultrices. A arcu cursus vitae congue. Maecenas sed enim "
                        "ut sem viverra aliquet eget sit amet. Placerat vestibulum lectus mauris ultrices eros in.")
            assert get_meta_description(files, "trim-long-description.md") == expected

    def test_trim_max_length_long_first_paragraph(self, build):
        _, files, mkdocs_yml, _ = build
        if "trim-max-length" in mkdocs_yml:
            expected = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
                        "labore et dolore magna aliqua. Neque convallis a cras semper auctor neque vitae tempus quam. "
                        "Lacus viverra")
            assert get_meta_description(files, "trim-long-first-paragraph.md") == expected


class TestFallbackIfShort:
    def test_fallback_if_short_first_paragraph(self, build):
        _, files, mkdocs_yml, _ = build
        if "fallback-if-short-default" in mkdocs_yml:
            expected = "Value of site_description on mkdocs.yml"
            assert get_meta_description(files, "first-paragraph.md") == expected

    def test_fallback_if_short_explicit_meta_description(self, build):
        _, files, mkdocs_yml, _ = build
        if "fallback-if-short-default" in mkdocs_yml:
            expected = "Short meta description."
            assert get_meta_description(files, "warning-short.md") == expected

    def test_fallback_if_short_min_length_first_paragraph(self, build):
        _, files, mkdocs_yml, _ = build
        if "fallback-if-short-min-length" in mkdocs_yml:
            expected = "Value of site_description on mkdocs.yml"
            assert get_meta_description(files, "first-paragraph.md") == expected

    def test_fallback_if_short_min_length_explicit_meta_description(self, build):
        _, files, mkdocs_yml, _ = build
        if "fallback-if-short-min-length" in mkdocs_yml:
            expected = "Short meta description."
            assert get_meta_description(files, "warning-short.md") == expected
