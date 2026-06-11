from pathlib import Path

import mr_dapa


ROOT = Path(__file__).resolve().parents[1]


def test_pyproject_declares_standard_distribution_metadata():
    text = (ROOT / "pyproject.toml").read_text()

    expected_fields = [
        'authors = [{ name = "xirhxq", email = "xirhxq@gmail.com" }]',
        'maintainers = [{ name = "xirhxq", email = "xirhxq@gmail.com" }]',
        'license = "MIT"',
        'license-files = ["LICENSE"]',
        'keywords = [',
        'classifiers = [',
        '[project.urls]',
        'Homepage = "https://github.com/xirhxq/mr-dapa"',
        'Repository = "https://github.com/xirhxq/mr-dapa"',
        'Issues = "https://github.com/xirhxq/mr-dapa/issues"',
        'Changelog = "https://github.com/xirhxq/mr-dapa/blob/main/CHANGELOG.md"',
    ]

    for field in expected_fields:
        assert field in text


def test_docs_release_matches_package_version():
    namespace = {}
    exec((ROOT / "docs/conf.py").read_text(), namespace)

    assert namespace["release"] == mr_dapa.__version__


def test_release_metadata_is_consistent_for_1_0_1():
    pyproject = (ROOT / "pyproject.toml").read_text()
    citation = (ROOT / "CITATION.cff").read_text()

    assert 'version = "1.0.1"' in pyproject
    assert mr_dapa.__version__ == "1.0.1"
    assert "version: 1.0.1" in citation


def test_citation_file_contains_academic_metadata():
    text = (ROOT / "CITATION.cff").read_text()

    expected_fields = [
        "cff-version: 1.2.0",
        "title: mr-dapa",
        "given-names: Siyuan",
        "family-names: Yang",
        "orcid: https://orcid.org/0009-0001-7980-4524",
        "repository-code: https://github.com/xirhxq/mr-dapa",
    ]

    for field in expected_fields:
        assert field in text


def test_manifest_includes_repository_metadata_files():
    text = (ROOT / "MANIFEST.in").read_text()

    expected_fields = [
        "include CITATION.cff",
        "include CHANGELOG.md",
    ]

    for field in expected_fields:
        assert field in text
