import Link from 'next/link'
import { FormEvent, useEffect, useState } from 'react'
import { api } from '../lib/api'

type Deal = { id: number; title: string; amount: number; stage?: string; contact_id?: number }

type Contact = { id: number; name: string }

export default function DealsPage() {
  const [items, setItems] = useState<Deal[]>([])
  const [contacts, setContacts] = useState<Contact[]>([])
  const [title, setTitle] = useState('')
  const [amount, setAmount] = useState('0')
  const [stage, setStage] = useState('new')
  const [contactId, setContactId] = useState<number | undefined>(undefined)

  async function load() {
    const [ds, cs] = await Promise.all([
      api('/deals/'),
      api('/contacts/'),
    ])
    setItems(ds)
    setContacts(cs)
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault()
    await api('/deals/', { method: 'POST', body: JSON.stringify({ title, amount: parseFloat(amount), stage, contact_id: contactId }) })
    setTitle(''); setAmount('0'); setStage('new'); setContactId(undefined);
    await load()
  }

  useEffect(() => { load() }, [])

  return (
    <div className="container">
      <h1>Deals</h1>
      <nav>
        <Link href="/">Login</Link>
        <Link href="/contacts">Contacts</Link>
        <Link href="/inventory">Inventory</Link>
        <Link href="/sales">Sales Orders</Link>
      </nav>
      <form onSubmit={onCreate}>
        <input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Title" required />
        <input value={amount} onChange={e=>setAmount(e.target.value)} placeholder="Amount" type="number" step="0.01" />
        <input value={stage} onChange={e=>setStage(e.target.value)} placeholder="Stage" />
        <select value={contactId || ''} onChange={e=>setContactId(e.target.value ? Number(e.target.value) : undefined)}>
          <option value="">(no contact)</option>
          {contacts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <button type="submit">Create</button>
      </form>
      <table>
        <thead>
          <tr><th>ID</th><th>Title</th><th>Amount</th><th>Stage</th><th>Contact</th></tr>
        </thead>
        <tbody>
          {items.map(d => (
            <tr key={d.id}>
              <td>{d.id}</td>
              <td>{d.title}</td>
              <td>{d.amount}</td>
              <td>{d.stage || ''}</td>
              <td>{d.contact_id || ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
