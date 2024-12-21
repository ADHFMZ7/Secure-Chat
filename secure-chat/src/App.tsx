import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { LoginForm } from "@/components/login-form"
import { RegisterForm } from "@/components/register-form"

export default function App() {
  return (
    <div className="w-full max-w-sm border border-gray-300">
      <BrowserRouter basename="/">
        <div className="flex min-h-screen w-full items-center justify-center p-6 md:p-10 bg-gray-100">
          <Routes>
            <Route path="/" element={<p>Home</p>} />
            <Route path="/login" element={<LoginForm /> } />
            <Route path="/register" element={<RegisterForm /> } />
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  )
}