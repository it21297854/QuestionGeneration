import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from './AuthContext'

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('')
  const { login } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleLogin = async (event) => {
    event.preventDefault()

    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const result = await response.json()

      if (response.ok) {
        setMessage(result.message || 'Login successful')
        setMessageType('success')
        login(result.user._id, result.user.email, 'User')
        navigate('/Sub_Selection')
      } else {
        setMessage(result.message || 'Invalid email or password')
        setMessageType('danger')
      }
    } catch (error) {
      console.error('Login error:', error)
      setMessage(`An error occurred: ${error.message}`)
      setMessageType('danger')
    }
  }

  return (
    <div className='registration-container'>
      {/* Left Side - Image */}
      <div className='registration-image'>
        <img src='/static/Assets/images/back.jpg' alt='Login Image' />
      </div>

      {/* Right Side - Form */}
      <div className='registration-form'>
        <h1>Login</h1>
        {message && (
          <div className={`alert alert-${messageType}`}>{message}</div>
        )}
        <form id='loginForm' onSubmit={handleLogin}>
          <div className='form-group'>
            <label htmlFor='email'>Email</label>
            <input
              type='email'
              id='email'
              name='email'
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className='form-group'>
            <label htmlFor='password'>Password</label>
            <input
              type='password'
              id='password'
              name='password'
              value={formData.password}
              onChange={handleInputChange}
              required
            />
          </div>
          <button type='submit' className='btn'>
            Login
          </button>
        </form>
        <div className='login-link'>
          Don't have an account? <a href='#register'>Register here</a>
        </div>
      </div>
    </div>
  )
}

export default Login
