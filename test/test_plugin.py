import pytest
import glob
import tempfile
import os.path

from mkdocs.__main__ import build_command
from mkdocs.structure.files import File, Files

from bs4 import BeautifulSoup
from click.testing import CliRunner


mkdocs_yml_list = glob.glob("test/**.yml")
markdown_files_list = [file[len("test/docs/"):] for file in glob.glob("test/docs/**.md")]


def get_meta_description(files, markdown_file_path):
    html_file_path = files.get_file_from_path(markdown_file_path).abs_dest_path
    with open(html_file_path) as file:
        html = file.read()
        soup = BeautifulSoup(html, features="lxml")
        result = soup.find("meta", {"name": "description"})
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
        yield result, files, mkdocs_yml


class TestPlugin:
    def test_build(self, build):
        result, _, _ = build
        assert result.exit_code == 0

    def test_build_output(self, build):
        _, files, _ = build
        for f in files:
            assert os.path.isfile(f.abs_dest_path)

    def test_index_md(self, build):
        _, files, _ = build
        assert get_meta_description(files, "index.md") == \
               "For full documentation visit mkdocs.org."

    def test_first_paragraph(self, build):
        _, files, _ = build
        assert get_meta_description(files, "first_paragraph.md") == \
               "First paragraph."

    def test_first_paragraph_no_heading(self, build):
        _, files, _ = build
        assert get_meta_description(files, "first_paragraph_no_heading.md") == \
               "First paragraph."

    def test_no_paragraph(self, build):
        _, files, _ = build
        assert get_meta_description(files, "no_paragraph.md") == \
               "Value of site_description on mkdocs.yml"

    def test_first_paragraph_no_intro(self, build):
        _, files, _ = build
        assert get_meta_description(files, "first_paragraph_no_intro.md") == \
               "Value of site_description on mkdocs.yml"

    def test_front_matter_description(self, build):
        _, files, _ = build
        assert get_meta_description(files, "front_matter_description.md") == \
               "Value of meta description on front_matter_description.md"

    def test_escape_html_entities(self, build):
        _, files, _ = build
        assert get_meta_description(files, "escape_html_entities.md") == \
               "First paragraph with HTML entities: \"quotes\", 'single quotes', "\
               "<greater and less than>, &ampersand&."
