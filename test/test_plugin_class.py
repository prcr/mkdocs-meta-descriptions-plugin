from mkdocs_meta_descriptions_plugin.plugin import MetaDescription


class TestPluginClass:
    test_configuration = {
        "param": ""
    }

    def test_load_config_errors(self):
        errors, _ = MetaDescription().load_config({})
        assert errors == []

    def test_load_config_warnings(self):
        _, warnings = MetaDescription().load_config({})
        assert warnings == []

    def test_valid_plugin_options(self):
        plugin = MetaDescription()
        plugin.load_config(self.test_configuration)
        assert plugin.config == self.test_configuration

    def test_get_first_paragraph(self):
        test_html = """
            <h1>Heading 1</h1>
            <p>First paragraph</p>
            <img src="image.png"/>
            <p>Second paragraph</p>
            <ul>
                <li>One</li>
                <li>Two</li>
            </ul>
            <h2>Heading 2</h2>
            <p>First paragraph under h2</p>
            """
        expected = "First paragraph"
        assert MetaDescription().get_first_paragraph_text(test_html) == expected

    def test_get_first_paragraph_no_paragraph(self):
        test_html = """
            <h1>Heading 1</h1>
            <img src="image.png"/>
            <ul>
                <li>One</li>
                <li>Two</li>
            </ul>
            <h2>Heading 2</h2>
            <p>First paragraph under h2</p>
            """
        expected = None
        assert MetaDescription().get_first_paragraph_text(test_html) == expected

    def test_get_first_paragraph_no_heading(self):
        test_html = """
            <p>First paragraph</p>
            <img src="image.png"/>
            <p>Second paragraph</p>
            <ul>
                <li>One</li>
                <li>Two</li>
            </ul>
            <h2>Heading 2</h2>
            <p>First paragraph under h2</p>
            """
        expected = "First paragraph"
        assert MetaDescription().get_first_paragraph_text(test_html) == expected

    def test_get_first_paragraph_no_introduction(self):
        test_html = """
            <img src="image.png"/>
            <h2>Heading 2</h2>
            <p>First paragraph under h2</p>
            <img src="image.png"/>
            <p>Second paragraph under h2</p>
            <ul>
                <li>One</li>
                <li>Two</li>
            </ul>
            """
        expected = None
        assert MetaDescription().get_first_paragraph_text(test_html) == expected
