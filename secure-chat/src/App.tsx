import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { LoginForm } from "@/components/login-form"
import { RegisterForm } from "@/components/register-form"
import AuthProvider from './context/AuthContext'
import PrivateRoute from './components/protected-route'
import { ChatInterface } from './components/chat-interface'

export default function App() {

  return (
    // <div className="w-full max-w-sm border border-gray-300">
      <BrowserRouter basename="/">
        <AuthProvider>
          {/* <div className="flex min-h-screen w-full items-center justify-center p-6 md:p-10 bg-gray-100"> */}
            <Routes>
              <Route element={<PrivateRoute />}>
                <Route path="/" element={<ChatInterface/>} />
              </Route>
              <Route path="/login" element={<LoginForm /> } />
              <Route path="/register" element={<RegisterForm /> } />
              <Route path="*" element={<p>404</p>} />
            </Routes>
          {/* </div> */}
        </AuthProvider>
      </BrowserRouter>
    // </div>
  )
}