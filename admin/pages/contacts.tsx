import Layout from '../components/Layout'
import { FormEvent, useEffect, useState } from 'react'
import { api } from '../lib/api'

type Contact = { id: number; name: string; email?: string; phone?: string; company?: string }

export default function ContactsPage() {
  const [items, setItems] = useState<Contact[]>([])
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [company, setCompany] = useState('')

  async function load() {
    const data = await api('/contacts/')
    setItems(data)
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault()
    await api('/contacts/', { method: 'POST', body: JSON.stringify({ name, email, phone, company }) })
    setName(''); setEmail(''); setPhone(''); setCompany('');
    await load()
  }

  useEffect(() => { load() }, [])

  return (
    <Layout title="Contacts" subtitle="Manage your customer and partner relationships">
      <div className="card">
        <div className="card-header">Create New Contact</div>
        <form onSubmit={onCreate}>
          <div className="form-row">
            <div className="form-group">
              <label>Name *</label>
              <input value={name} onChange={e=>setName(e.target.value)} placeholder="John Doe" required />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="john@example.com" />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Phone</label>
              <input value={phone} onChange={e=>setPhone(e.target.value)} placeholder="+1 234 567 8900" />
            </div>
            <div className="form-group">
              <label>Company</label>
              <input value={company} onChange={e=>setCompany(e.target.value)} placeholder="Acme Corp" />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Create Contact</button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">All Contacts ({items.length})</div>
        {items.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Company</th>
                </tr>
              </thead>
              <tbody>
                {items.map(c => (
                  <tr key={c.id}>
                    <td><strong>{c.name}</strong></td>
                    <td>{c.email || '—'}</td>
                    <td>{c.phone || '—'}</td>
                    <td>{c.company || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">👥</div>
            <p>No contacts yet. Create your first contact above.</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
