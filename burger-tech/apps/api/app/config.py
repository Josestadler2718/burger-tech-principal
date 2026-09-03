import os
from pathlib import Path

from dotenv import load_dotenv

API_DIR = Path(__file__).resolve().parent.parent

load_dotenv(API_DIR / ".env")


def _env(nome: str, padrao: str) -> str:
    valor = os.getenv(nome)
    return valor if valor else padrao


JWT_SECRET_CLIENTE = _env("JWT_SECRET_CLIENTE", "dev-inseguro-cliente-troque-isto")
JWT_SECRET_ADMIN = _env("JWT_SECRET_ADMIN", "dev-inseguro-admin-troque-isto")
JWT_ALGORITHM = _env("JWT_ALGORITHM", "HS256")
JWT_EXPIRA_MINUTOS_CLIENTE = int(_env("JWT_EXPIRA_MINUTOS_CLIENTE", "1440"))
JWT_EXPIRA_MINUTOS_ADMIN = int(_env("JWT_EXPIRA_MINUTOS_ADMIN", "480"))

DATABASE_PATH = API_DIR / _env("DATABASE_PATH", "database/burger_tech.db")
SCHEMA_PATH = API_DIR / "database" / "schema.sql"

# Onde ficam as fotos dos produtos enviadas pelo painel admin (servidas como
# arquivo estático em /uploads — veja main.py)
UPLOADS_DIR = API_DIR / "uploads"
UPLOADS_PRODUTOS_DIR = UPLOADS_DIR / "produtos"

CORS_ORIGINS = [o.strip() for o in _env("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if o.strip()]
