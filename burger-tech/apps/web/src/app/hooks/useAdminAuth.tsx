import { createContext, useContext, useEffect, useState } from "react";
import type { Administrador } from "@/app/types";
import { loginAdmin } from "@/app/lib/api";

const CHAVE_TOKEN = "bt_admin_token";
const CHAVE_ADMIN = "bt_admin_dados";

type AdminAuthContextValue = {
  administrador: Administrador | null;
  token: string | null;
  carregando: boolean;
  login: (email: string, senha: string) => Promise<void>;
  logout: () => void;
};

const AdminAuthContext = createContext<AdminAuthContextValue | null>(null);

export function AdminAuthProvider({ children }: { children: React.ReactNode }) {
  const [administrador, setAdministrador] = useState<Administrador | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const tokenSalvo = localStorage.getItem(CHAVE_TOKEN);
    const adminSalvo = localStorage.getItem(CHAVE_ADMIN);
    if (tokenSalvo && adminSalvo) {
      setToken(tokenSalvo);
      setAdministrador(JSON.parse(adminSalvo));
    }
    setCarregando(false);
  }, []);

  const login = async (email: string, senha: string) => {
    const resposta = await loginAdmin({ email, senha });
    localStorage.setItem(CHAVE_TOKEN, resposta.access_token);
    localStorage.setItem(CHAVE_ADMIN, JSON.stringify(resposta.administrador));
    setToken(resposta.access_token);
    setAdministrador(resposta.administrador);
  };

  const logout = () => {
    localStorage.removeItem(CHAVE_TOKEN);
    localStorage.removeItem(CHAVE_ADMIN);
    setToken(null);
    setAdministrador(null);
  };

  return (
    <AdminAuthContext.Provider value={{ administrador, token, carregando, login, logout }}>
      {children}
    </AdminAuthContext.Provider>
  );
}

export function useAdminAuth() {
  const contexto = useContext(AdminAuthContext);
  if (!contexto) throw new Error("useAdminAuth precisa estar dentro de <AdminAuthProvider>");
  return contexto;
}
