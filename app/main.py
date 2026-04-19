"""
🐾 Apperritos Backend - Punto de entrada de la API

Este archivo configura FastAPI con:
- CORS habilitado (para que el frontend se conecte)
- Ruta de salud (/health) para verificar que la API funciona
- Inclusión de routers por entidad (se agregarán en fases posteriores)

📌 Para correr el servidor en desarrollo:
    cd backend
    .\venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pets as pets_router

# ─────────────────────────────────────────────
# Crear la instancia de FastAPI
# ─────────────────────────────────────────────
app = FastAPI(
    title="🐾 Apperritos API",
    description="API para gestión de mascotas: vacunas, citas, comida y más.",
    version="0.1.0",
)

# ─────────────────────────────────────────────
# Configurar CORS
# Permite que el frontend (Expo/React Native) se conecte
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# Ruta de salud (health check)
# ─────────────────────────────────────────────
@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica que la API está funcionando correctamente."""
    return {"status": "ok", "message": "🐾 Apperritos API está corriendo"}


# ─────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────
app.include_router(pets_router.router)

