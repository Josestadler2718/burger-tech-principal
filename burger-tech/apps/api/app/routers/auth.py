import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth_cliente import criar_token_cliente, get_usuario_atual, hash_senha, verificar_senha
from app.db import get_db
from app.schemas import LoginIn, RegistoIn, TokenOut, UsuarioOut

router = APIRouter(prefix="/auth", tags=["autenticação de cliente"])


def _linha_para_usuario(linha: sqlite3.Row) -> UsuarioOut:
    return UsuarioOut(id=linha["id"], nome=linha["nome"], email=linha["email"], telefone=linha["telefone"])


@router.post("/registo", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def registar(dados: RegistoIn, db: sqlite3.Connection = Depends(get_db)) -> TokenOut:
    existente = db.execute("SELECT id FROM usuarios WHERE email = ?", (dados.email,)).fetchone()
    if existente is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe uma conta com este e-mail")

    cursor = db.execute(
        "INSERT INTO usuarios (nome, email, senha_hash, telefone) VALUES (?, ?, ?, ?)",
        (dados.nome, dados.email, hash_senha(dados.senha), dados.telefone),
    )
    db.commit()

    usuario = db.execute("SELECT * FROM usuarios WHERE id = ?", (cursor.lastrowid,)).fetchone()
    token = criar_token_cliente(usuario["id"], usuario["email"])
    return TokenOut(access_token=token, usuario=_linha_para_usuario(usuario))


@router.post("/login", response_model=TokenOut)
def login(dados: LoginIn, db: sqlite3.Connection = Depends(get_db)) -> TokenOut:
    usuario = db.execute("SELECT * FROM usuarios WHERE email = ?", (dados.email,)).fetchone()
    if usuario is None or not verificar_senha(dados.senha, usuario["senha_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha incorretos")

    token = criar_token_cliente(usuario["id"], usuario["email"])
    return TokenOut(access_token=token, usuario=_linha_para_usuario(usuario))


@router.get("/me", response_model=UsuarioOut)
def eu(usuario: sqlite3.Row = Depends(get_usuario_atual)) -> UsuarioOut:
    return _linha_para_usuario(usuario)
