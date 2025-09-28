# plots_route.py (no Gateway)
from fastapi import APIRouter, HTTPException, Depends, Header, Query
from typing import Optional
import httpx
import uuid
from ..core.auth import authenticate_token
import os

FAST_URL = os.getenv("FAST_URL", "http://fastapi:8001")

router = APIRouter(prefix="/plots", tags=["plots"])

@router.post("/eeg")
async def generate_eeg_plot(
    request_body: dict,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    auth_data = await authenticate_token(token)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{FAST_URL}/plots/eeg",
            headers={"Authorization": f"Bearer {token}"},
            json=request_body
        )

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        return resp.json()


@router.delete("/cache")
async def clear_plot_cache(
    authorization: Optional[str] = Header(None),
    edf_file_id: Optional[uuid.UUID] = Query(None, description="ID do EDF para limpar cache")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token necessário")

    token = authorization.replace("Bearer ", "")
    await authenticate_token(token)

    params = {"edf_file_id": str(edf_file_id)} if edf_file_id else {}

    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f"{FAST_URL}/plots/cache",
            headers={"Authorization": f"Bearer {token}"},
            params=params
        )

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        return resp.json()