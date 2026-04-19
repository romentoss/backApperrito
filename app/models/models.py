"""
🐾 Modelos Pydantic - Entidades del dominio

Estos modelos se usan para:
- Validar datos de entrada (requests)
- Serializar datos de salida (responses)
- Documentar automáticamente la API en /docs

📌 Usamos BaseModel de Pydantic v2 con Field() para
documentación clara de cada campo.
"""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# 👤 Usuario
# ─────────────────────────────────────────────
class UserBase(BaseModel):
    email: str = Field(..., description="Email del usuario")
    display_name: str = Field(..., description="Nombre visible del usuario")
    photo_url: Optional[str] = Field(None, description="URL de foto de perfil")


class UserCreate(UserBase):
    """Datos necesarios para crear un usuario."""
    pass


class UserResponse(UserBase):
    """Datos que se devuelven al cliente."""
    id: str = Field(..., description="ID único del usuario en Firestore")
    created_at: datetime = Field(..., description="Fecha de creación")


# ─────────────────────────────────────────────
# 🐕 Mascota
# ─────────────────────────────────────────────
class PetBase(BaseModel):
    name: str = Field(..., description="Nombre de la mascota")
    species: Literal["dog", "cat", "bird", "rabbit", "other"] = Field(
        ..., description="Tipo de animal"
    )
    breed: Optional[str] = Field(None, description="Raza")
    birth_date: Optional[str] = Field(None, description="Fecha de nacimiento (ISO 8601)")
    weight: Optional[float] = Field(None, description="Peso en kilogramos")
    photo_url: Optional[str] = Field(None, description="URL de la foto")
    notes: Optional[str] = Field(None, description="Notas adicionales")


class PetCreate(PetBase):
    """Datos necesarios para registrar una mascota."""
    pass


class PetResponse(PetBase):
    """Datos que se devuelven al cliente."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


# ─────────────────────────────────────────────
# 💉 Vacuna
# ─────────────────────────────────────────────
class VaccineBase(BaseModel):
    name: str = Field(..., description="Nombre de la vacuna")
    applied_date: str = Field(..., description="Fecha de aplicación")
    next_dose_date: Optional[str] = Field(None, description="Fecha de próxima dosis")
    veterinarian: Optional[str] = Field(None, description="Nombre del veterinario")
    notes: Optional[str] = Field(None, description="Notas")


class VaccineCreate(VaccineBase):
    """Datos necesarios para registrar una vacuna."""
    pass


class VaccineResponse(VaccineBase):
    """Datos que se devuelven al cliente."""
    id: str
    pet_id: str
    created_at: datetime


# ─────────────────────────────────────────────
# 📅 Cita
# ─────────────────────────────────────────────
class AppointmentBase(BaseModel):
    type: Literal["grooming", "vet"] = Field(..., description="Tipo de cita")
    title: str = Field(..., description="Descripción corta de la cita")
    date_time: str = Field(..., description="Fecha y hora (ISO 8601)")
    location: Optional[str] = Field(None, description="Dirección o nombre del lugar")
    professional: Optional[str] = Field(None, description="Nombre del profesional")
    notes: Optional[str] = Field(None, description="Notas adicionales")
    completed: bool = Field(False, description="Si la cita ya se realizó")


class AppointmentCreate(AppointmentBase):
    """Datos necesarios para crear una cita."""
    pass


class AppointmentResponse(AppointmentBase):
    """Datos que se devuelven al cliente."""
    id: str
    pet_id: str
    created_at: datetime


# ─────────────────────────────────────────────
# 🍖 Registro de comida
# ─────────────────────────────────────────────
class FoodRecordBase(BaseModel):
    brand: str = Field(..., description="Marca del alimento")
    product: str = Field(..., description="Nombre del producto")
    quantity: float = Field(..., description="Cantidad comprada")
    unit: Literal["kg", "lb", "bag", "can"] = Field(..., description="Unidad de medida")
    purchase_date: str = Field(..., description="Fecha de compra")
    price: Optional[float] = Field(None, description="Precio de la compra")
    notes: Optional[str] = Field(None, description="Notas")


class FoodRecordCreate(FoodRecordBase):
    """Datos necesarios para registrar una compra de comida."""
    pass


class FoodRecordResponse(FoodRecordBase):
    """Datos que se devuelven al cliente."""
    id: str
    pet_id: str
    created_at: datetime


# ─────────────────────────────────────────────
# 🔄 Compra periódica
# ─────────────────────────────────────────────
class PeriodicPurchaseBase(BaseModel):
    brand: str = Field(..., description="Marca del alimento")
    product: str = Field(..., description="Nombre del producto")
    quantity: float = Field(..., description="Cantidad por compra")
    unit: Literal["kg", "lb", "bag", "can"] = Field(..., description="Unidad")
    frequency_value: int = Field(..., description="Cada cuánto se compra (número)")
    frequency_unit: Literal["days", "weeks", "months"] = Field(
        ..., description="Unidad de frecuencia"
    )
    is_active: bool = Field(True, description="Si la compra periódica está activa")
    notes: Optional[str] = Field(None, description="Notas")


class PeriodicPurchaseCreate(PeriodicPurchaseBase):
    """Datos para crear una compra periódica."""
    pass


class PeriodicPurchaseResponse(PeriodicPurchaseBase):
    """Datos que se devuelven al cliente."""
    id: str
    pet_id: str
    last_purchase_date: Optional[str]
    next_purchase_date: Optional[str]
    created_at: datetime
    updated_at: datetime
