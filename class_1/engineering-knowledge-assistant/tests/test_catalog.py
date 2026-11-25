"""Acceptance tests for the Class 1 document catalog homework."""

from pathlib import Path

import pytest

from engineering_knowledge_assistant.catalog import (
    DocumentInfo,
    build_manifest,
    describe_document,
    discover_documents,
    is_supported_document,
)


def test_supported_extensions_are_case_insensitive(tmp_path: Path) -> None:
    pdf = tmp_path / "manual.PDF"
    pdf.write_text("placeholder", encoding="utf-8")
    assert is_supported_document(pdf) is True


def test_unsupported_extension_is_rejected(tmp_path: Path) -> None:
    image = tmp_path / "diagram.png"
    image.write_text("placeholder", encoding="utf-8")
    assert is_supported_document(image) is False


def test_directory_is_not_a_document(tmp_path: Path) -> None:
    folder = tmp_path / "manuals"
    folder.mkdir()
    assert is_supported_document(folder) is False


def test_discover_documents_is_recursive_and_sorted(tmp_path: Path) -> None:
    (tmp_path / "z.txt").write_text("z", encoding="utf-8")
    nested = tmp_path / "subfolder"
    nested.mkdir()
    (nested / "b.md").write_text("b", encoding="utf-8")
    (nested / "a.pdf").write_text("a", encoding="utf-8")
    (tmp_path / "skip.csv").write_text("skip", encoding="utf-8")

    found = discover_documents(tmp_path)

    assert [path.relative_to(tmp_path).as_posix() for path in found] == [
        "subfolder/a.pdf",
        "subfolder/b.md",
        "z.txt",
    ]


def test_discover_nonexistent_root_returns_empty_list(tmp_path: Path) -> None:
    assert discover_documents(tmp_path / "missing") == []


def test_discover_file_as_root_raises(tmp_path: Path) -> None:
    file_path = tmp_path / "not-a-folder.txt"
    file_path.write_text("content", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        discover_documents(file_path)


def test_describe_document_returns_relative_metadata(tmp_path: Path) -> None:
    folder = tmp_path / "manuals"
    folder.mkdir()
    document = folder / "Safety.PDF"
    document.write_bytes(b"12345")

    info = describe_document(document, tmp_path)

    assert info == DocumentInfo(
        name="Safety.PDF",
        relative_path="manuals/Safety.PDF",
        extension=".pdf",
        size_bytes=5,
    )


def test_describe_unsupported_document_raises(tmp_path: Path) -> None:
    document = tmp_path / "diagram.png"
    document.write_text("image", encoding="utf-8")
    with pytest.raises(ValueError):
        describe_document(document, tmp_path)


def test_describe_path_outside_root_raises(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    with pytest.raises(ValueError):
        describe_document(outside, root)


def test_build_manifest_composes_discovery_and_description(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "a.md").write_text("world!", encoding="utf-8")

    manifest = build_manifest(tmp_path)

    assert [item.relative_path for item in manifest] == ["a.md", "b.txt"]
    assert [item.size_bytes for item in manifest] == [6, 5]

#Test añadidos
def test_build_manifest_empty_or_missing_root(tmp_path: Path) -> None:
    assert build_manifest(tmp_path / "does_not_exist") == []


def test_discover_ignores_directories_with_supported_extension(
    tmp_path: Path,
) -> None:
    fake_pdf_dir = tmp_path / "tricky.pdf"
    fake_pdf_dir.mkdir()
    assert discover_documents(tmp_path) == []