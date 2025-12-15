import Link from 'next/link'
import { FormEvent, useEffect, useState } from 'react'
import { api } from '../lib/api'

type SaleOrder = { id: number; order_number: string; contact_id?: number; status: string; total: number }
type Contact = { id: number; name: string }

export default function SalesPage() {
  const [items, setItems] = useState<SaleOrder[]>([])
  const [contacts, setContacts] = useState<Contact[]>([])
  const [orderNumber, setOrderNumber] = useState('')
  const [contactId, setContactId] = useState<number | undefined>(undefined)
  const [status, setStatus] = useState('draft')
  const [total, setTotal] = useState('0')

  async function load() {
    const [orders, cs] = await Promise.all([
      api('/sales/'),
      api('/contacts/'),
    ])
    setItems(orders)
    setContacts(cs)
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault()
    await api('/sales/', {
      method: 'POST',
      body: JSON.stringify({
        order_number: orderNumber,
        contact_id: contactId,
        status,
        total: parseFloat(total),
      }),
    })
    setOrderNumber(''); setContactId(undefined); setStatus('draft'); setTotal('0');
    await load()
  }

  useEffect(() => { load() }, [])

  return (
    <div className="container">
      <h1>Sales Orders</h1>
      <nav>
        <Link href="/">Login</Link>
        <Link href="/contacts">Contacts</Link>
        <Link href="/deals">Deals</Link>
        <Link href="/inventory">Inventory</Link>
      </nav>
      <form onSubmit={onCreate}>
        <input value={orderNumber} onChange={e=>setOrderNumber(e.target.value)} placeholder="Order Number" required />
        <select value={contactId || ''} onChange={e=>setContactId(e.target.value ? Number(e.target.value) : undefined)}>
          <option value="">(no contact)</option>
          {contacts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <select value={status} onChange={e=>setStatus(e.target.value)}>
          <option value="draft">Draft</option>
          <option value="confirmed">Confirmed</option>
          <option value="shipped">Shipped</option>
          <option value="invoiced">Invoiced</option>
        </select>
        <input value={total} onChange={e=>setTotal(e.target.value)} placeholder="Total" type="number" step="0.01" />
        <button type="submit">Create</button>
      </form>
      <table>
        <thead>
          <tr><th>ID</th><th>Order #</th><th>Contact ID</th><th>Status</th><th>Total</th></tr>
        </thead>
        <tbody>
          {items.map(o => (
            <tr key={o.id}>
              <td>{o.id}</td>
              <td>{o.order_number}</td>
              <td>{o.contact_id || ''}</td>
              <td>{o.status}</td>
              <td>${o.total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
