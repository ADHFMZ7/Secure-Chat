import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { LoginForm } from "@/components/login-form"
import { RegisterForm } from "@/components/register-form"
import { AuthProvider } from './context/AuthContext'
import PrivateRoute from './components/protected-route'
import { ChatInterface } from './components/chat-interface'

export default function App() {

  return (
      <BrowserRouter basename="/">
        <AuthProvider>
            <Routes>
              <Route element={<PrivateRoute />}>
                <Route path="/" element={<ChatInterface/>} />
              </Route>
              <Route path="/login" element={<LoginForm /> } />
              <Route path="/register" element={<RegisterForm /> } />
              <Route path="*" element={<p>404</p>} />
            </Routes>
        </AuthProvider>
      </BrowserRouter>
  )
}