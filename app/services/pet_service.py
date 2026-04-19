"""
🐕 PetService — Lógica de negocio para mascotas en Firestore

Encapsula todas las operaciones de Firestore para la colección:
  users/{userId}/pets/{petId}

Los servicios no conocen FastAPI — sólo Firestore y Pydantic.
"""

from datetime import datetime, timezone
from typing import List, Optional

from google.cloud.firestore_v1 import DocumentSnapshot
from app.firebase.client import get_firestore_client
from app.models.models import PetCreate, PetBase


def _doc_to_dict(doc: DocumentSnapshot) -> dict:
    """Convierte un DocumentSnapshot a dict con el id incluido."""
    data = doc.to_dict() or {}
    data["id"] = doc.id
    # Convertir Timestamps a ISO strings
    for field in ("createdAt", "updatedAt", "birthDate"):
        if field in data and hasattr(data[field], "isoformat"):
            data[field] = data[field].isoformat()
    return data


def _pet_ref(user_id: str, pet_id: Optional[str] = None):
    """Referencia a la colección o documento de mascotas de un usuario."""
    db = get_firestore_client()
    col = db.collection("users").document(user_id).collection("pets")
    return col.document(pet_id) if pet_id else col


def get_all_pets(user_id: str) -> List[dict]:
    """Obtiene todas las mascotas del usuario, ordenadas por fecha de creación."""
    col = _pet_ref(user_id)
    docs = col.order_by("createdAt").stream()
    return [_doc_to_dict(doc) for doc in docs]


def get_pet_by_id(user_id: str, pet_id: str) -> Optional[dict]:
    """Obtiene una mascota por ID. Retorna None si no existe."""
    doc = _pet_ref(user_id, pet_id).get()
    if not doc.exists:
        return None
    return _doc_to_dict(doc)


def create_pet(user_id: str, data: PetCreate) -> dict:
    """Crea una nueva mascota y retorna el documento creado."""
    col = _pet_ref(user_id)
    now = datetime.now(timezone.utc)

    pet_data = data.model_dump(exclude_none=True)
    pet_data.update({
        "userId": user_id,
        "createdAt": now,
        "updatedAt": now,
    })

    doc_ref = col.document()
    doc_ref.set(pet_data)

    # Leer el documento recién creado para devolver datos completos
    return _doc_to_dict(doc_ref.get())


def update_pet(user_id: str, pet_id: str, data: PetCreate) -> Optional[dict]:
    """
    Actualiza los campos de una mascota.
    Retorna None si la mascota no pertenece al usuario o no existe.
    """
    doc_ref = _pet_ref(user_id, pet_id)
    doc = doc_ref.get()
    if not doc.exists:
        return None

    update_data = data.model_dump(exclude_none=True)
    update_data["updatedAt"] = datetime.now(timezone.utc)

    doc_ref.update(update_data)
    return _doc_to_dict(doc_ref.get())


def delete_pet(user_id: str, pet_id: str) -> bool:
    """Elimina una mascota. Retorna True si existía, False si no."""
    doc_ref = _pet_ref(user_id, pet_id)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    doc_ref.delete()
    return True
