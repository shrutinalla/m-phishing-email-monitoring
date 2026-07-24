// src/context/AuthContext.jsx

import { createContext, useContext, useState } from "react";
import {
  getToken,
  saveToken,
  removeToken,
} from "../utils/token";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(getToken());

  const login = (jwtToken) => {
    saveToken(jwtToken);
    setToken(jwtToken);
  };

  const logout = () => {
    removeToken();
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        login,
        logout,
        isLoggedIn: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);