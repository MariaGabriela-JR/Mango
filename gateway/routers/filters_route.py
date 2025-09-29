from fastapi import APIRouter, HTTPException, Request
import httpx
import os

router = APIRouter()
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8001")

@router.get("/discover")
async def proxy_discover():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{FASTAPI_URL}/api/filters/discover")
        return resp.json()

@router.post("/{file_name}/apply")
async def proxy_apply(file_name: str, request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{FASTAPI_URL}/api/filters/{file_name}/apply", json=payload)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
