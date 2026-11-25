# Burger Tech

O Burger Tech é um sistema de pedidos que eu criei para uma hamburgueria. Ele começou no projeto em grupo da faculdade, o [Science Burger](https://github.com/Josestadler2718/science-burger-backend), em que eu cuidava só da API de login. Depois, a ideia cresceu e virou um sistema completo, com site, painel e back-end no mesmo repositório.

## Como ele funciona

Imagina a hamburgueria funcionando com ele:

- **Pelo site**, o cliente vê o cardápio, monta o carrinho e escolhe se quer entrega ou retirada. Ele também pode criar uma conta e acompanhar os pedidos.
- **Na mesa**, tem um QR code. O cliente escaneia e já cai no cardápio, com o pedido ligado à comanda daquela mesa, sem precisar chamar o garçom.
- **No painel da loja**, a equipe entra com um login próprio e vê mesas e pedidos chegando em tempo real. Por ali também dá para subir as fotos dos produtos.

## Com o que eu fiz

No back-end usei **Python com FastAPI** e um banco **SQLite** com 13 tabelas. Parte das regras de negócio fica direto no banco, com triggers e índices, para que os dados continuem certos mesmo fora da API. Também escrevi testes com **pytest** para o login, as mesas e os pedidos.

No front-end usei **React com TypeScript**, Vite e Tailwind. As atualizações em tempo real do painel funcionam com WebSocket.

## Quer rodar na sua máquina?

O passo a passo completo está no [README do projeto](burger-tech/README.md). Em resumo: a API sobe com `uvicorn` dentro de `burger-tech/apps/api`, e o site com `npm run dev` a partir de `burger-tech/`.

---

Feito por José Augusto, estudante de Ciência da Computação na Unigranrio | Afya.
[LinkedIn](https://www.linkedin.com/in/jos%C3%A9-augusto-stadler/) · [GitHub](https://github.com/Josestadler2718)
