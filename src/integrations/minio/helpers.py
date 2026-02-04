from __future__ import annotations

import os
import re
import unicodedata
from uuid import UUID, uuid4

_slug_re = re.compile(r"[^a-z0-9]+")
_multi_sep_re = re.compile(r"[_-]{2,}")


def slugify(value: str, *, max_length: int = 80) -> str:
    value = (value or "").strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = _slug_re.sub("_", value).strip("_")
    value = _multi_sep_re.sub("_", value)
    return (value or "item")[:max_length].strip("_")


def sanitize_filename(filename: str, *, max_length: int = 120) -> str:
    filename = os.path.basename(filename or "upload")
    filename = filename.replace("\x00", "").strip()
    filename = re.sub(r"\s+", "_", filename)
    filename = re.sub(r"[^A-Za-z0-9._-]", "", filename)

    if not filename:
        filename = "upload"

    root, ext = os.path.splitext(filename)
    if len(filename) > max_length:
        keep = max_length - len(ext)
        root = root[: max(1, keep)]
        filename = f"{root}{ext}"
    return filename


def build_media_object_name(
    *,
    media_type: str,
    original_filename: str,
    mosque_name: str | None = None,
    mosque_id: UUID | None = None,
) -> str:
    """
    Returns a relative path INSIDE the provider directory.
    Example: "mosques/al_fateh/<media_id>/photo.jpg"
    Provider will turn it into: "<media_directory>/mosques/al_fateh/<media_id>/photo.jpg"
    """
    safe_filename = sanitize_filename(original_filename)

    # Prefer mosque_id for stability if available
    if mosque_id is not None:
        mosque_part = str(mosque_id)
    elif mosque_name:
        mosque_part = slugify(mosque_name, max_length=60)
    else:
        mosque_part = "unknown_mosque"

    return f"mosques/{mosque_part}/{media_type}/{safe_filename}"


_ext_re = re.compile(r"^[a-z0-9]{1,10}$", re.IGNORECASE)


def safe_extension_from_filename(filename: str) -> str:
    """
    Extracts extension without dot, lowercased. Returns "" if none/unsafe.
    """
    _, ext = os.path.splitext(filename or "")
    ext = ext[1:].lower() if ext.startswith(".") else ""
    if not ext or not _ext_re.match(ext):
        return ""
    return ext


def generate_random_filename(
    *, original_filename: str | None = None, ext: str | None = None
) -> str:
    """
    Generates a non-reproducible filename (random UUID4), keeping an extension if provided.
    Example: "c2b9c1f2a8f84f68a0e6e8b3f8b2a8a1.jpg"
    """
    if ext is None and original_filename:
        ext = safe_extension_from_filename(original_filename)

    token = uuid4().hex  # random, non-reproducible
    return f"{token}.{ext}" if ext else token
