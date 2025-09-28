# chunks_route.py (Gateway)
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import httpx
import uuid
import os
from ..core.auth import authenticate_token

FAST_URL = os.getenv("FASTAPI_URL", "http://fastapi:8001")

router = APIRouter(prefix="/chunks", tags=["chunks"])

@router.get("/edf/{edf_file_id}/summary")
async def get_edf_chunks_summary(
    edf_file_id: uuid.UUID,
    authorization: Optional[str] = Header(None)
):
    """Proxy para resumo dos chunks de um EDF."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    await authenticate_token(token)

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FAST_URL}/chunks/edf/{edf_file_id}/summary",
            headers={"Authorization": f"Bearer {token}"}
        )

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        return resp.json()


@router.get("/edf/{edf_file_id}/chunk/{chunk_index}")
async def get_specific_chunk(
    edf_file_id: uuid.UUID,
    chunk_index: int,
    authorization: Optional[str] = Header(None)
):
    """Proxy para obter dados de um chunk específico de um EDF."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    await authenticate_token(token)

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{FAST_URL}/chunks/edf/{edf_file_id}/chunk/{chunk_index}",
            headers={"Authorization": f"Bearer {token}"}
        )

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        return resp.json()
