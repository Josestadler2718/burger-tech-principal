import { createContext, useContext, useEffect, useState } from "react";
import type { Usuario } from "@/app/types";
import { loginCliente, registarCliente } from "@/app/lib/api";

const CHAVE_TOKEN = "bt_cliente_token";
const CHAVE_USUARIO = "bt_cliente_usuario";

type ClienteAuthContextValue = {
  usuario: Usuario | null;
  token: string | null;
  carregando: boolean;
  login: (email: string, senha: string) => Promise<void>;
  registar: (nome: string, email: string, senha: string, telefone?: string) => Promise<void>;
  logout: () => void;
};

const ClienteAuthContext = createContext<ClienteAuthContextValue | null>(null);

export function ClienteAuthProvider({ children }: { children: React.ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const tokenSalvo = localStorage.getItem(CHAVE_TOKEN);
    const usuarioSalvo = localStorage.getItem(CHAVE_USUARIO);
    if (tokenSalvo && usuarioSalvo) {
      setToken(tokenSalvo);
      setUsuario(JSON.parse(usuarioSalvo));
    }
    setCarregando(false);
  }, []);

  const salvarSessao = (novoToken: string, novoUsuario: Usuario) => {
    localStorage.setItem(CHAVE_TOKEN, novoToken);
    localStorage.setItem(CHAVE_USUARIO, JSON.stringify(novoUsuario));
    setToken(novoToken);
    setUsuario(novoUsuario);
  };

  const login = async (email: string, senha: string) => {
    const resposta = await loginCliente({ email, senha });
    salvarSessao(resposta.access_token, resposta.usuario);
  };

  const registar = async (nome: string, email: string, senha: string, telefone?: string) => {
    const resposta = await registarCliente({ nome, email, senha, telefone });
    salvarSessao(resposta.access_token, resposta.usuario);
  };

  const logout = () => {
    localStorage.removeItem(CHAVE_TOKEN);
    localStorage.removeItem(CHAVE_USUARIO);
    setToken(null);
    setUsuario(null);
  };

  return (
    <ClienteAuthContext.Provider value={{ usuario, token, carregando, login, registar, logout }}>
      {children}
    </ClienteAuthContext.Provider>
  );
}

export function useClienteAuth() {
  const contexto = useContext(ClienteAuthContext);
  if (!contexto) throw new Error("useClienteAuth precisa estar dentro de <ClienteAuthProvider>");
  return contexto;
}
