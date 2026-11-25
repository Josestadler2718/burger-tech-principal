# Burger Tech

Sistema web de pedidos para uma hamburgueria, com site de delivery, pedidos pela mesa via QR code e painel administrativo. Comecei a partir do projeto em grupo da faculdade ([Science Burger – Backend](https://github.com/Josestadler2718/science-burger-backend)) e fui transformando num sistema completo, com front-end e back-end no mesmo repositório.

## O que o sistema faz

- **Site público:** cardápio, carrinho, cadastro e login de clientes, e pedidos para entrega ou retirada.
- **Pedido pela mesa:** cada mesa tem um QR code próprio. O cliente escaneia e cai direto no cardápio, já vinculado à comanda daquela mesa.
- **Painel administrativo:** login separado para a equipe da loja, com mesas e pedidos atualizados em tempo real via WebSocket e upload de fotos dos produtos.

## Tecnologias

| Parte | Tecnologias |
|---|---|
| Back-end (`apps/api`) | Python, FastAPI, SQLite, pytest |
| Front-end (`apps/web`) | React 18, TypeScript, Vite, Tailwind CSS |

O banco tem 13 tabelas (usuários, administradores, mesas, comandas, pedidos, pagamentos e outras), e parte das regras de negócio fica garantida por triggers e índices no próprio banco, em `apps/api/database/schema.sql`. O back-end tem testes de autenticação, mesas e pedidos.

## Como rodar

O passo a passo completo está no [README do projeto](burger-tech/README.md). Em resumo: a API sobe com `uvicorn` dentro de `burger-tech/apps/api`, e o front-end com `npm run dev` a partir de `burger-tech/`.

## Autor

José Augusto, estudante de Ciência da Computação na Unigranrio | Afya.
[LinkedIn](https://www.linkedin.com/in/jos%C3%A9-augusto-stadler/) · [GitHub](https://github.com/Josestadler2718)
