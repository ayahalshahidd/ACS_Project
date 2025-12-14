import { ReactNode } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Layout.css'

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  const navigate = useNavigate()
  
  // VULNERABLE: Retrieving user data from localStorage. 
  // A student can open DevTools and change "role": "student" to "admin" 
  // to make the Admin link appear instantly.
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const isLoggedIn = !!user.id;

  const handleLogout = () => {
    localStorage.removeItem('user');
    // Also clear session cookie for the backend
    document.cookie = "sid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    navigate('/login');
  };

  return (
    <div className="layout">
      <header className="header">
        <div className="container">
          <nav className="nav">
            <Link to="/courses">Catalog</Link>
            
            {isLoggedIn ? (
              <>
                {/* Visible to Students and Admins */}
                <Link to="/dashboard">My Dashboard</Link>

                {/* VULNERABLE: UI-only role protection for Instructor Dashboard */}
                {user.role === 'instructor' && (
                  <Link to="/instructor" style={{ color: '#00ff88' }}>Instructor</Link>
                )}

                {/* VULNERABLE: UI-only role protection for Admin Panel */}
                {(user.role === 'admin' || user.role === 'registrar') && (
                  <Link to="/admin" style={{ color: '#ffcc00' }}>Admin Panel</Link>
                )}

                <button onClick={handleLogout} className="logout-btn">
                  Logout ({user.email})
                </button>
              </>
            ) : (
              <Link to="/login" className="login-link">Login</Link>
            )}
          </nav>
        </div>
      </header>

      <main className="main">
        <div className="container">
          {children}
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <p>&copy; 2024 Advanced Cyber Security - Project 1 Baseline</p>
        </div>
      </footer>
    </div>
  )
}

export default Layout