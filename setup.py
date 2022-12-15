from setuptools import setup

file = open("README.md", "r")
LONG_DESCRIPTION = file.read()
file.close()

file = open("requirements.txt", "r")
DEPENDENCIES = file.readlines()
file.close()

del file

setup(
    name="mkdocs-meta-descriptions-plugin",
    version="0.0.1",
    description="Generate meta descriptions from the first paragraphs in your MkDocs pages",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="mkdocs meta description seo paragraph",
    url="https://github.com/prcr/mkdocs-meta-descriptions-plugin",
    author="Paulo Ribeiro",
    author_email="paulo@diffraction.pt",
    license="MIT",
    python_requires=">=3",
    install_requires=DEPENDENCIES,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    packages=["mkdocs_meta_descriptions_plugin"],
    entry_points={
        "mkdocs.plugins": [
            "meta-descriptions = mkdocs_meta_descriptions_plugin.plugin:MetaDescription"
        ]
    },
    use_scm_version={
        "local_scheme": "no-local-version"
    },
    setup_requires=["setuptools_scm"]
)
