import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './components/AuthContext'
import MainLayout from './components/MainLayout'
import Register from './components/User_Register'
import Login from './components/User_Login'
import HomePage from './components/HomePage'
import Quize from './components/Quize'
import Subjects from './components/SubSelection'

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <MainLayout>
          <Routes>
            <Route path='/' element={<HomePage />} />
            <Route path='/User_Register' element={<Register />} />
            <Route path='/User_Login' element={<Login />} />
            <Route path='/Sub_Selection' element={<Subjects />} />
            <Route path='/Quize/software engineering' element={<Quize />} />
          </Routes>
        </MainLayout>
      </Router>
    </AuthProvider>
  )
}

export default App
