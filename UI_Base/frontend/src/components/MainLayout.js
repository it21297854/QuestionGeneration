import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const MainLayout = ({ children }) => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <>
      <nav className="navbar">
        <ul>
         
          {user ? (
            <>
              <li><button  onClick={handleLogout}>Logout</button></li>
 
			    <li><Link to="/Quize">Refresh </Link></li>
            </>
          ) : (
            <>
			 <li><Link to="/">Home</Link></li>
              <li><Link to="/User_login">Login</Link></li>
              <li><Link to="/User_Register">Register</Link></li>
            </>
          )}
        </ul>
      </nav>

      <main>{children}</main>
    </>
  );
};

export default MainLayout;
