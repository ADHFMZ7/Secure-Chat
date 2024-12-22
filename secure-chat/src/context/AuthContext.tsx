import React, { useContext, createContext, useState, useEffect } from "react";

// Define types for AuthContext
interface AuthContextType {
  user: { username: string; user_id: number } | null;
  token: string;
  loginAction: (data: FormData) => Promise<void>;
  logOut: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<{ username: string; user_id: number } | null>(() => {
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [token, setToken] = useState<string>(localStorage.getItem("token") || "");

  const loginAction = async (data: FormData) => {
    try {
      const response = await fetch("https://chat.aldasouqi.com/login", {
        method: "POST",
        body: data,
      });

      if (!response.ok) {
        throw new Error("Login failed. Please check your credentials.");
      }

      const res = await response.json();
      console.log("Response: ", res);
      if (res.access_token && res.username && res.user_id) {
        const userData = { username: res.username, user_id: res.user_id };
        setUser(userData);
        setToken(res.access_token);
        localStorage.setItem("token", res.access_token);
        localStorage.setItem("user", JSON.stringify(userData));
        return; // Let the caller decide what to do next (e.g., navigate)
      }
      console.error("Error response body:", res);
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logOut = () => {
    setUser(null);
    setToken("");
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  };

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, loginAction, logOut }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export { AuthProvider, useAuth };