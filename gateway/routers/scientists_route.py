from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import httpx
import os

router = APIRouter()

# Configuração do REST API
RESTAPI_URL = os.getenv("RESTAPI_URL", "http://restapi:8000")

# =============================================================================
# MODELS
# =============================================================================

class ScientistRegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    institution: str
    specialization: str

class ScientistLoginRequest(BaseModel):
    email: str
    password: str

# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/register")
async def register_scientist(request: ScientistRegisterRequest):
    """
    Registra um novo cientista no sistema
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            scientist_payload = {
                "email": request.email,
                "password": request.password,
                "first_name": request.first_name,
                "last_name": request.last_name,
                "institution": request.institution,
                "specialization": request.specialization
            }
            
            response = await client.post(
                f"{RESTAPI_URL}/restapi/scientists/register/",
                json=scientist_payload
            )
            
            if response.status_code == 201:
                scientist_data = response.json()
                return {
                    "status": "success",
                    "message": "Cientista registrado com sucesso",
                    "scientist_id": scientist_data.get("id"),
                    "email": scientist_data.get("email"),
                    "is_verified": scientist_data.get("is_verified", False),
                    "verification_token": scientist_data.get("verification_token"),
                    "registration_token": scientist_data.get("registration_token")
                }
            else:
                error_detail = response.json().get('error', response.text)
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_detail
                )
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Unavailable service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.post("/login")
async def login_scientist(request: ScientistLoginRequest):
    """
    Login de cientista - retorna tokens JWT
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            login_payload = {
                "email": request.email,
                "password": request.password
            }
            
            response = await client.post(
                f"{RESTAPI_URL}/restapi/auth/login/scientists/",
                json=login_payload
            )
            
            if response.status_code == 200:
                login_data = response.json()
                return {
                    "status": "success",
                    "message": "Login realizado com sucesso",
                    "access_token": login_data.get("access"),
                    "refresh_token": login_data.get("refresh"),
                    "scientist": {
                        "id": login_data.get("id"),
                        "scientist_id": login_data.get("scientist_id"),
                        "email": login_data.get("email"),
                        "first_name": login_data.get("first_name"),
                        "last_name": login_data.get("last_name"),
                        "institution": login_data.get("institution"),
                        "specialization": login_data.get("specialization"),
                        "is_verified": login_data.get("is_verified", False)
                    }
                }
            else:
                error_detail = response.json().get('detail', 'Invalid credentials')
                raise HTTPException(status_code=401, detail=error_detail)
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Unavailable service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/profile")
async def get_scientist_profile(authorization: Optional[str] = Header(None)):
    """
    Obtém o perfil do cientista autenticado
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            response = await client.get(
                f"{RESTAPI_URL}/restapi/scientists/profile/",
                headers=headers
            )
            
            if response.status_code == 200:
                profile_data = response.json()
                return {
                    "status": "success",
                    "scientist": profile_data
                }
            else:
                raise HTTPException(status_code=response.status_code, detail="Error obtaining profile")
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Unavailable service: {str(e)}")

@router.post("/logout")
async def logout_scientist(
    logout_request: dict,
    authorization: Optional[str] = Header(None)
):
    """
    Logout do cientista - invalida o refresh token
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    refresh_token = logout_request.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is necessary")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            response = await client.post(
                f"{RESTAPI_URL}/restapi/auth/logout/",
                json={"refresh": refresh_token},
                headers=headers
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Logout made with success"
                }
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json().get('detail', 'Error on logout')
                )
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Unavailable service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
