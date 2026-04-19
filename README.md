# 🐾 Apperritos - Backend API
# FastAPI + Firebase

Este backend sigue arquitectura por capas:
- **routers/**: Endpoints HTTP (controladores)
- **services/**: Lógica de negocio
- **models/**: Modelos de datos (Pydantic)
- **schemas/**: Esquemas de request/response
- **firebase/**: Cliente y configuración de Firebase

## Deploy en Render

Configuración recomendada para Render:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Python version**: definida en `runtime.txt` como `python-3.11.11`
- **Variable recomendada en Render**: `PYTHON_VERSION=3.11.11` (evita que Render use 3.14)

Variables de entorno requeridas:

- `FIREBASE_STORAGE_BUCKET`
- `FIREBASE_SERVICE_ACCOUNT_JSON` (JSON completo de la service account en una sola línea)

Notas:

- En local puedes seguir usando `FIREBASE_SERVICE_ACCOUNT_PATH`.
- En Render es mejor usar `FIREBASE_SERVICE_ACCOUNT_JSON` para no depender de archivos en disco.
