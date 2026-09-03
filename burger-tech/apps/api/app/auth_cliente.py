import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import JWT_ALGORITHM, JWT_EXPIRA_MINUTOS_CLIENTE, JWT_SECRET_CLIENTE
from app.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# auto_error=False: em rotas de mesa o login é opcional, então tratamos o
# "sem token" manualmente em vez de deixar o FastAPI recusar de cara.
_bearer_scheme = HTTPBearer(auto_error=False)


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def criar_token_cliente(usuario_id: int, email: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRA_MINUTOS_CLIENTE)
    claims = {
        "sub": str(usuario_id),
        "email": email,
        "tipo_conta": "cliente",
        "exp": expira,
    }
    return jwt.encode(claims, JWT_SECRET_CLIENTE, algorithm=JWT_ALGORITHM)


def _decodificar_token_cliente(token: str) -> dict:
    try:
        claims = jwt.decode(token, JWT_SECRET_CLIENTE, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

    if claims.get("tipo_conta") != "cliente":
        # Garante que um token de administrador nunca é aceito aqui, mesmo que
        # tenha sido assinado com a mesma chave por engano em algum ponto.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido para esta rota")

    return claims


def get_usuario_atual(
    credenciais: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
    db: sqlite3.Connection = Depends(get_db),
) -> sqlite3.Row:
    if credenciais is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")

    claims = _decodificar_token_cliente(credenciais.credentials)
    usuario = db.execute("SELECT * FROM usuarios WHERE id = ?", (claims["sub"],)).fetchone()
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return usuario


def get_usuario_opcional(
    credenciais: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
    db: sqlite3.Connection = Depends(get_db),
) -> Optional[sqlite3.Row]:
    if credenciais is None:
        return None
    try:
        claims = _decodificar_token_cliente(credenciais.credentials)
    except HTTPException:
        return None
    return db.execute("SELECT * FROM usuarios WHERE id = ?", (claims["sub"],)).fetchone()
