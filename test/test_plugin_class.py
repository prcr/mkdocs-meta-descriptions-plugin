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
