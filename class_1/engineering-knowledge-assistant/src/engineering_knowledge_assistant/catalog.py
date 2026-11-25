"""Discover and describe documents for the course project.

The functions in this module are intentionally left for students to complete.
Read the tests in ``tests/test_catalog.py`` before implementing them.
"""

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


@dataclass(frozen=True, slots=True)
class DocumentInfo:
    """Metadata recorded for one supported document."""

    name: str
    relative_path: str
    extension: str
    size_bytes: int


def is_supported_document(path: Path) -> bool:
    """Return True when path is a regular file with a supported extension.

    Extension matching must be case-insensitive. Directories are not documents
    """
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def discover_documents(root: Path) -> list[Path]:
    """Find supported documents recursively, sorted by relative POSIX path."""
    if not root.exists():
        return []

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    documents = []

    for path in root.rglob("*"):
        if is_supported_document(path):
            documents.append(path)

    return sorted(documents, key=lambda path: path.relative_to(root).as_posix())


def describe_document(path: Path, root: Path) -> DocumentInfo:
    """Create metadata for path, using a path relative to root."""
    if not is_supported_document(path):
        raise ValueError(f"Unsupported document: {path}")

    relative_path = path.resolve().relative_to(root.resolve())

    return DocumentInfo(
        name=path.name,
        relative_path=relative_path.as_posix(),
        extension=path.suffix.lower(),
        size_bytes=path.stat().st_size,
    )


def build_manifest(root: Path) -> list[DocumentInfo]:
    """Return metadata for every supported document below root."""
    manifest = []

    for path in discover_documents(root):
        info = describe_document(path, root)
        manifest.append(info)

    return manifest
