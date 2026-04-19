"""
🔥 Cliente Firebase - Inicialización del SDK Admin

Este módulo inicializa Firebase Admin SDK para el backend.
Se usa para acceder a Firestore, Auth y Storage desde el servidor.

📌 CONFIGURACIÓN:
1. Ve a Firebase Console → Configuración del proyecto → Cuentas de servicio
2. Genera una nueva clave privada (JSON)
3. Guarda el archivo como: backend/firebase-service-account.json
4. NUNCA subas este archivo a Git (ya está en .gitignore)

📌 Variables de entorno necesarias en .env:
    FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
    FIREBASE_STORAGE_BUCKET=tu-proyecto.appspot.com
"""

import json
import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, storage

load_dotenv()

_service_account_path = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase-service-account.json"
)
_service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
_storage_bucket = os.getenv("FIREBASE_STORAGE_BUCKET", "")


def _init_firebase():
    """Inicializa Firebase Admin SDK de forma lazy (solo si no está ya inicializado)."""
    if not firebase_admin._apps:
        if _service_account_json:
            try:
                cred_info = json.loads(_service_account_json)
                cred = credentials.Certificate(cred_info)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    "FIREBASE_SERVICE_ACCOUNT_JSON no contiene un JSON válido."
                ) from exc
        else:
            if not os.path.isfile(_service_account_path):
                raise RuntimeError(
                    f"No se encontró el archivo de credenciales Firebase: '{_service_account_path}'. "
                    "Consulta backend/README.md para configurarlo."
                )
            cred = credentials.Certificate(_service_account_path)
        firebase_admin.initialize_app(cred, {"storageBucket": _storage_bucket})


def get_firestore_client():
    """Retorna el cliente de Firestore para operaciones de base de datos."""
    _init_firebase()
    return firestore.client()


def get_storage_bucket():
    """Retorna el bucket de Storage para subir/descargar archivos."""
    _init_firebase()
    return storage.bucket()
