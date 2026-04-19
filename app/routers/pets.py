"""
🐕 Router de mascotas — /api/pets

Endpoints:
  GET    /api/pets            → Listar todas las mascotas del usuario
  POST   /api/pets            → Crear una nueva mascota
  GET    /api/pets/{pet_id}   → Obtener una mascota por ID
  PUT    /api/pets/{pet_id}   → Actualizar una mascota
  DELETE /api/pets/{pet_id}   → Eliminar una mascota

Todos los endpoints requieren autenticación con Firebase Auth token.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.models import PetCreate, PetResponse
from app.firebase.auth_middleware import get_current_user_id
from app.services import pet_service

router = APIRouter(
    prefix="/api/pets",
    tags=["pets"],
)


@router.get("/", response_model=List[PetResponse])
async def list_pets(user_id: str = Depends(get_current_user_id)):
    """Retorna todas las mascotas del usuario autenticado."""
    pets = pet_service.get_all_pets(user_id)
    return pets


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(
    data: PetCreate,
    user_id: str = Depends(get_current_user_id),
):
    """Crea una nueva mascota para el usuario autenticado."""
    pet = pet_service.create_pet(user_id, data)
    return pet


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(
    pet_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Retorna una mascota específica por ID."""
    pet = pet_service.get_pet_by_id(user_id, pet_id)
    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada.",
        )
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
async def update_pet(
    pet_id: str,
    data: PetCreate,
    user_id: str = Depends(get_current_user_id),
):
    """Actualiza los datos de una mascota."""
    pet = pet_service.update_pet(user_id, pet_id, data)
    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada.",
        )
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(
    pet_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Elimina una mascota por ID."""
    deleted = pet_service.delete_pet(user_id, pet_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada.",
        )
