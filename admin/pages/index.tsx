import { FormEvent, useState } from 'react'
import { api, setToken } from '../lib/api'
import { useRouter } from 'next/router'

export default function LoginPage() {
  const router = useRouter()
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      setToken(res.token)
      localStorage.setItem('user', JSON.stringify(res.user))
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">⚡ WorkOS</h1>
        <p className="login-subtitle">Your modern business operating system</p>
        <form className="login-form" onSubmit={onSubmit}>
          <input 
            value={username} 
            onChange={e => setUsername(e.target.value)} 
            placeholder="Username" 
            required
          />
          <input 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            placeholder="Password" 
            type="password"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        {error && <p style={{color:'var(--danger)', marginTop: '16px', textAlign: 'center'}}>{error}</p>}
        <p style={{marginTop: '24px', fontSize: '13px', color: 'var(--gray-600)', textAlign: 'center'}}>
          Demo: admin/admin123, sales/sales123, viewer/viewer123
        </p>
      </div>
    </div>
  )
}
