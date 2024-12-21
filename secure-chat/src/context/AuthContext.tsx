import React, { useContext, createContext, useState } from "react";

// Define types for AuthContext
interface AuthContextType {
  user: any; // Replace `any` with your user type
  token: string;
  loginAction: (data: FormData) => Promise<void>;
  logOut: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any>(null); // Replace `any` with your user type
  const [token, setToken] = useState<string>(localStorage.getItem("token") || "");

  const loginAction = async (data: FormData) => {
    try {
      const response = await fetch("http://chat.aldasouqi.com/login", {
        method: "POST",
        body: data,
      });

      if (!response.ok) {
        throw new Error("Login failed. Please check your credentials.");
      }

      const res = await response.json();
      console.log("Response: ", res );
      if (res.access_token) {
        setUser(res.access_token);
        setToken(res.access_token);
        localStorage.setItem("token", res.access_token);
        return; // Let the caller decide what to do next (e.g., navigate)
      }
      console.error("Error response body:", res);
      throw new Error(res.message || "Unknown error occurred.");
    } catch (err: any) {
      console.error("Login error:", err.message || err);
      throw err; // Propagate the error to the caller
    }
  };

  const logOut = () => {
    setUser(null);
    setToken("");
    localStorage.removeItem("token"); // Use the correct key
  };

  return (
    <AuthContext.Provider value={{ token, user, loginAction, logOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
