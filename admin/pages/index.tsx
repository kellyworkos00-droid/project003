import { FormEvent, useState } from 'react'
import { api, setToken } from '../lib/api'
import Link from 'next/link'

export default function LoginPage() {
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('admin')
  const [error, setError] = useState('')

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    try {
      const res = await api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      setToken(res.token)
      window.location.href = '/contacts'
    } catch (err: any) {
      setError(err.message || 'Login failed')
    }
  }

  return (
    <div className="container">
      <h1>OpenERP Admin — Login</h1>
      <nav>
        <Link href="/contacts">Contacts</Link>
        <Link href="/deals">Deals</Link>
      </nav>
      <form onSubmit={onSubmit}>
        <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
        <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" />
        <button type="submit">Login</button>
      </form>
      {error && <p style={{color:'crimson'}}>{error}</p>}
      <p style={{opacity:0.7}}>Default: admin / admin (set via env on backend)</p>
    </div>
  )
}
