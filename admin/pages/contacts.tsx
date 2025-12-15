import Link from 'next/link'
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
    <div className="container">
      <h1>Contacts</h1>
      <nav>
        <Link href="/">Login</Link>
        <Link href="/deals">Deals</Link>
      </nav>
      <form onSubmit={onCreate}>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Name" required />
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" />
        <input value={phone} onChange={e=>setPhone(e.target.value)} placeholder="Phone" />
        <input value={company} onChange={e=>setCompany(e.target.value)} placeholder="Company" />
        <button type="submit">Create</button>
      </form>
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Company</th></tr>
        </thead>
        <tbody>
          {items.map(c => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>{c.name}</td>
              <td>{c.email || ''}</td>
              <td>{c.phone || ''}</td>
              <td>{c.company || ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
