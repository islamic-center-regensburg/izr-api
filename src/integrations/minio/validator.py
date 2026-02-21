from fastapi import HTTPException, UploadFile
from typing import Iterable


async def validate_upload_type(files: list[UploadFile], allowed: Iterable[str]) -> None:
    for file in files:
        if file.content_type not in allowed:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported media type: {file.content_type}. Allowed: {sorted(allowed)}",
            )
