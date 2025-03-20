import React, { useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AuthContext } from './AuthContext'
import './navbar.css'

const MainLayout = ({ children }) => {
  const { user, logout } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <>
      <nav className='navbar'>
        <div className='navbar-container'>
          <div className='navbar-brand'>
            <Link to='/' className='logo'>
              <span className='logo-text-primary'>QUIZ</span>
              <span className='logo-text-secondary'>APP</span>
            </Link>
          </div>

          <div className='navbar-menu'>
            {user ? (
              <>
                <Link to='/Que_Bank' className='navbar-link'>
                  Question Bank
                </Link>
                <Link
                  to='/Sub_Selection'
                  className='navbar-link subject-selection'
                >
                  Subject Selection
                </Link>
              </>
            ) : (
              <>
                <Link to='/' className='navbar-link'>
                  Home
                </Link>
                <Link to='/User_login' className='navbar-link'>
                  Login
                </Link>
                <Link to='/User_Register' className='navbar-link'>
                  Register
                </Link>
              </>
            )}
          </div>

          {/* {user && (
            <div className='user-profile'>
              <div className='user-avatar'>
                <img
                  src='/user-avatar.png'
                  alt='User'
                  className='avatar-image'
                />
              </div>
            </div>
          )} */}

          {user && (
            <button onClick={handleLogout} className='navbar-button logout-btn'>
              Logout
            </button>
          )}
        </div>
      </nav>

      <main>{children}</main>
    </>
  )
}

export default MainLayout
