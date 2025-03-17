import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from './AuthContext'

const Register = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    address: '',
    contact: '',
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

  const handleRegister = async (event) => {
    event.preventDefault()

    try {
      const response = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const result = await response.json()

      if (response.ok) {
        setMessage(result.message || 'Registration successful')
        setMessageType('success')
        login(result.user._id, result.user.email, 'User')
        navigate('/quize') // Redirect to the dashboard after registration
      } else {
        setMessage(result.message || 'Registration failed')
        setMessageType('danger')
      }
    } catch (error) {
      console.error('Error during registration:', error)
      setMessage(`An error occurred: ${error.message}`)
      setMessageType('danger')
    }
  }

  return (
    <div className='registration-container'>
      {/* Left Side - Image */}
      <div className='registration-image'>
        <img src='/static/Assets/images/back.jpg' alt='Registration' />
      </div>

      {/* Right Side - Form */}
      <div className='registration-form'>
        <h1>Register</h1>
        {message && (
          <div className={`alert alert-${messageType}`}>{message}</div>
        )}
        <form id='registerForm' onSubmit={handleRegister}>
          <div className='form-group'>
            <label htmlFor='fullName'>Full Name</label>
            <input
              type='text'
              id='fullName'
              name='fullName'
              value={formData.fullName}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className='form-group'>
            <label htmlFor='address'>Address</label>
            <input
              type='text'
              id='address'
              name='address'
              value={formData.address}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className='form-group'>
            <label htmlFor='contact'>Contact</label>
            <input
              type='text'
              id='contact'
              name='contact'
              value={formData.contact}
              onChange={handleInputChange}
              required
            />
          </div>
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
            Register
          </button>
        </form>
        <div className='login-link'>
          Already have an account? <a href='#login'>Login here</a>
        </div>
      </div>
    </div>
  )
}

export default Register
