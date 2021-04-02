from setuptools import setup, find_packages


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
    description="Generate a meta description from the first paragraph in each MkDocs page",
    long_description=LONG_DESCRIPTION,
    keywords="mkdocs meta description",
    url="https://github.com/prcr/mkdocs-meta-descriptions-plugin",
    author="Paulo Ribeiro",
    author_email="paulo@diffraction.pt",
    license="MIT",
    python_requires=">=3",
    install_requires=DEPENDENCIES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "meta-descriptions = mkdocs_meta_descriptions_plugin.plugin:MetaDescription"
        ]
    }
)
