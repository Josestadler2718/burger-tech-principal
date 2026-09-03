# Burger Tech

Sistema completo do Science Burger Tech: site público de delivery, fluxo de
pedido por mesa (QR code) e painel administrativo — com um back-end próprio
em Python.

```
burger-tech/
├── apps/
│   ├── web/   ← front-end (React 18 + Vite + TypeScript + Tailwind v4)
│   └── api/   ← back-end (Python + FastAPI + SQLite)
```

Veja [apps/api/database/README.md](apps/api/database/README.md) para entender
o desenho do banco de dados (o mais importante é o sistema de mesas/comandas).

## Rodando em desenvolvimento

Precisa de **Node.js** (18+) e **Python** (3.11+) instalados. Os dois
serviços rodam em paralelo, em dois terminais separados.

### 1. Back-end (API)

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\activate          # Windows (no Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # Windows (no Linux/Mac: cp .env.example .env)
uvicorn app.main:app --reload
```

Na primeira vez que sobe, a API cria sozinha o banco `apps/api/database/burger_tech.db`
a partir do `database/schema.sql` (13 tabelas + seed de categorias/produtos/mesas)
e imprime no terminal os links `/m/<token>` de cada mesa (os QR codes apontam
pra essas URLs, no front-end). A API fica em `http://127.0.0.1:8000` — a
documentação interativa está em `http://127.0.0.1:8000/docs`.

Crie o primeiro administrador do painel (uma vez só):

```bash
python -m app.criar_admin
```

### 2. Front-end (web)

Num segundo terminal, a partir da raiz do repositório:

```bash
npm install
npm run dev
```

Abre em `http://localhost:5173`. O Vite já está configurado para
redirecionar `/api/*` e `/ws/*` para `http://127.0.0.1:8000` (veja
`apps/web/vite.config.ts`), então não precisa mexer em CORS nem em URLs
durante o desenvolvimento.

## As três áreas do sistema

- **Site público** (`/`, `/cardapio`, `/login`, `/registo`, `/pedidos`, ...) —
  cardápio, carrinho e pedidos de entrega/retirada.
- **Mesa via QR code** (`/m/<token>`) — sem nenhum link no site público; cada
  mesa tem o seu próprio link, impresso/gerado a partir do que a API mostra
  ao criar o banco.
- **Painel administrativo** (`/admin/login`, `/admin`) — login separado da
  equipe da loja (tabela `administradores`, distinta de `usuarios`), também
  sem link público. Mostra mesas e pedidos em tempo real via WebSocket.

## Testes do back-end

```bash
cd apps/api
.venv\Scripts\activate
pytest
```
