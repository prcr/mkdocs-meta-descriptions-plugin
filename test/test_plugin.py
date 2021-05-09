import pytest
import glob
import tempfile
import os.path
import filecmp

from mkdocs.__main__ import build_command
from mkdocs.structure.files import File, Files

from bs4 import BeautifulSoup
from click.testing import CliRunner


mkdocs_yml_list = glob.glob("test/*.yml")
markdown_files_list = [file[len("test/docs/"):] for file in glob.glob("test/docs/**/*.md", recursive=True)]


def get_meta_description(files, markdown_file_path):
    html_file_path = files.get_file_from_path(markdown_file_path).abs_dest_path
    with open(html_file_path) as file:
        html = file.read()
        soup = BeautifulSoup(html, features="lxml")
        result = soup.select_one("meta[name=\"description\"]")
        return result["content"] if result else None


@pytest.fixture(scope="module",
                params=[True, False],
                ids=["use-directory-urls", "no-directory-urls"])
def use_directory_urls(request):
    flag = "--use-directory-urls" if request.param else "--no-directory-urls"
    return flag, request.param


@pytest.fixture(scope="module",
                params=mkdocs_yml_list)
def build(request, use_directory_urls):
    mkdocs_yml = request.param
    with tempfile.TemporaryDirectory() as tempdir:
        result = CliRunner().invoke(build_command,
                                    ["--config-file", mkdocs_yml,
                                     "--site-dir", tempdir,
                                     use_directory_urls[0]])
        files = Files([File(file,
                            os.path.join(os.getcwd(), "test/docs/"),
                            tempdir,
                            use_directory_urls[1]) for file in markdown_files_list])
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
        expected = (
            "For full documentation visit mkdocs.org."
        )
        assert get_meta_description(files, "index.md") == expected

    def test_first_paragraph(self, build):
        _, files, _, _ = build
        expected = (
            "First paragraph."
        )
        assert get_meta_description(files, "first_paragraph.md") == expected

    def test_first_paragraph_no_heading(self, build):
        _, files, _, _ = build
        expected = (
            "First paragraph."
        )
        assert get_meta_description(files, "first_paragraph_no_heading.md") == expected

    def test_first_paragraph_no_paragraph(self, build):
        _, files, mkdocs_yml, _ = build
        if "no_site_description" in mkdocs_yml:
            expected = (
                None
            )
        else:
            expected = (
                "Value of site_description on mkdocs.yml"
            )
        assert get_meta_description(files, "first_paragraph_no_paragraph.md") == expected

    def test_first_paragraph_no_intro(self, build):
        _, files, mkdocs_yml, _ = build
        if "no_site_description" in mkdocs_yml:
            expected = (
                None
            )
        else:
            expected = (
                "Value of site_description on mkdocs.yml"
            )

        assert get_meta_description(files, "first_paragraph_no_intro.md") == expected

    def test_front_matter_description(self, build):
        _, files, _, _ = build
        expected = (
            "Value of meta description on front_matter_description.md"
        )
        assert get_meta_description(files, "front_matter_description.md") == expected

    def test_escape_html_entities(self, build):
        _, files, _, _ = build
        expected = (
            "First paragraph with HTML entities: \"quotes\", 'single quotes', "
            "<greater and less than>, &ampersand&."
        )
        assert get_meta_description(files, "escape_html_entities.md") == expected


class TestExport:
    def test_export_csv_build(self, build):
        result, files, mkdocs_yml, _ = build
        if "export_csv" in mkdocs_yml and "no_site_url" not in mkdocs_yml:
            expected = (
                f"INFO    -  [meta-descriptions] Reading meta descriptions from {len(files)} HTML pages"
            )
            assert expected in result.output

    def test_export_csv_build_no_site_url(self, build):
        result, _, mkdocs_yml, _ = build
        if "export_csv" in mkdocs_yml:
            if "no_site_url.yml" in mkdocs_yml:
                expected = (
                    "WARNING -  [meta-descriptions] Can't export meta descriptions to CSV "
                    "because site_url is not defined."
                )
                assert expected in result.output

    def test_export_csv_output(self, build):
        _, files, mkdocs_yml, use_directory_urls = build
        if "export_csv.yml" in mkdocs_yml:
            index_path = files.get_file_from_path("index.md").abs_dest_path
            csv_path = index_path.replace("index.html", "meta_descriptions.csv")
            if use_directory_urls:
                assert filecmp.cmp("test/meta_descriptions.csv", csv_path)
            else:
                assert filecmp.cmp("test/meta_descriptions_no_directory_urls.csv", csv_path)

    def test_export_csv_output_no_site_description(self, build):
        _, files, mkdocs_yml, use_directory_urls = build
        if "export_csv_no_site_description.yml" in mkdocs_yml:
            index_path = files.get_file_from_path("index.md").abs_dest_path
            csv_path = index_path.replace("index.html", "meta_descriptions.csv")
            if use_directory_urls:
                assert filecmp.cmp("test/meta_descriptions_no_site_description.csv", csv_path)
            else:
                assert filecmp.cmp("test/meta_descriptions_no_site_description_no_directory_urls.csv", csv_path)
