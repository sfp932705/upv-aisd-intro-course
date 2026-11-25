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
    """
    return path.suffix.lower() in SUPPORTED_EXTENSIONS and not path.is_dir()


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
        raise NotADirectoryError
    docs = [f for f in root.rglob("*") if is_supported_document(f)]
    return sorted(docs, key=lambda x: x.relative_to(root))


def describe_document(path: Path, root: Path) -> DocumentInfo:
    """Create metadata for path, using a path relative to root.

    Store the original filename, a POSIX relative path, a lower-case extension,
    and the file size in bytes. Raise ValueError for unsupported files or paths
    outside root.
    """
    if not is_supported_document(path):
        raise ValueError
    return DocumentInfo(
        name=path.name,
        relative_path=path.relative_to(root).as_posix(),
        extension=path.suffix.lower(),
        size_bytes=path.stat().st_size,
    )


def build_manifest(root: Path) -> list[DocumentInfo]:
    """Return metadata for every supported document below root.

    Use discover_documents and describe_document rather than duplicating logic.
    """
    return [describe_document(x, root) for x in discover_documents(root)]
