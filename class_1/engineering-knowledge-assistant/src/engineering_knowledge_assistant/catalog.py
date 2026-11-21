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
    """Return True when path is a regular file with a supported extension."""
    if not path.is_file():
        return False
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def discover_documents(root: Path) -> list[Path]:
    """Recursively find supported documents below root."""
    if not root.exists():
        return []
    if not root.is_dir():
        raise NotADirectoryError(f"{root} is not a directory")

    found_files = []
    for item in root.rglob("*"):
        if is_supported_document(item):
            found_files.append(item)

    return sorted(found_files, key=lambda p: p.relative_to(root).as_posix())


def describe_document(path: Path, root: Path) -> DocumentInfo:
    """Create metadata for path, using a path relative to root."""
    if not is_supported_document(path):
        raise ValueError(f"{path} is not a supported document")

    return DocumentInfo(
        name=path.name,
        relative_path=path.relative_to(root).as_posix(),
        extension=path.suffix.lower(),
        size_bytes=path.stat().st_size,
    )


def build_manifest(root: Path) -> list[DocumentInfo]:
    """Compose the previous functions; do not duplicate their logic."""
    documents = discover_documents(root)
    manifest = []
    for doc_path in documents:
        info = describe_document(doc_path, root)
        manifest.append(info)
    return manifest
