import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(result.message || 'Login successful');
        setMessageType('success');
        login(result.user._id, result.user.email, 'Player');
        navigate('/Quize');
      } else {
        setMessage(result.message || 'Invalid email or password');
        setMessageType('danger');
      }
    } catch (error) {
      console.error('Login error:', error);
      setMessage('An error occurred while trying to log in');
      setMessageType('danger');
    }
  };

  return (
    <div className="container">
      <h1>Login</h1>
      {message && <div className={`alert alert-${messageType}`}>{message}</div>}
      <form id="loginForm" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn">Login</button>
      </form>
      <div className="register-link">
        Don't have an account? <a href="#contact">Register here</a>
      </div>
    </div>
  );
};

export default Login;