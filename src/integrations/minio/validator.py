from fastapi import HTTPException, UploadFile
from typing import Iterable


async def validate_upload_type(file: UploadFile, allowed: Iterable[str]) -> None:
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type: {file.content_type}. Allowed: {sorted(allowed)}",
        )
