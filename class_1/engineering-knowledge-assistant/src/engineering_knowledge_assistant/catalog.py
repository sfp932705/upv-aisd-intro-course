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

    Extension matching must be case-insensitive. Directories are not documents.
    TODO: implement this function.
    """
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def discover_documents(root: Path) -> list[Path]:
    """Recursively find supported documents below root.

    Return paths rooted at root, sorted by their relative POSIX path.
    Return an empty list when root does not exist. Raise NotADirectoryError when
    root exists but is not a directory.
    TODO: implement this function.
    """
    if not root.exists():
        return []

    if not root.is_dir():
        raise NotADirectoryError(root)

    documents = [path for path in root.rglob("*") if is_supported_document(path)]

    return sorted(
        documents,
        key=lambda path: path.relative_to(root).as_posix(),
    )


def describe_document(path: Path, root: Path) -> DocumentInfo:
    """Create metadata for path, using a path relative to root.

    Store the original filename, a POSIX relative path, a lower-case extension,
    and the file size in bytes. Raise ValueError for unsupported files or paths
    outside root.
    TODO: implement this function.
    """
    if not is_supported_document(path):
        raise ValueError(f"Unsupported document: {path}")

    try:
        relative_path = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"Path {path} is outside root {root}") from exc

    return DocumentInfo(
        name=path.name,
        relative_path=relative_path,
        extension=path.suffix.lower(),
        size_bytes=path.stat().st_size,
    )


def build_manifest(root: Path) -> list[DocumentInfo]:
    """Return metadata for every supported document below root.

    Use discover_documents and describe_document rather than duplicating logic.
    TODO: implement this function.
    """
    return [describe_document(path, root) for path in discover_documents(root)]
