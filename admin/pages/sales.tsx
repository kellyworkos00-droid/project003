import Layout from '../components/Layout'
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'secondary'
      case 'confirmed': return 'info'
      case 'shipped': return 'warning'
      case 'invoiced': return 'success'
      default: return 'secondary'
    }
  }

  return (
    <Layout title="Sales Orders" subtitle="Track customer orders and fulfillment">
      <div className="card">
        <div className="card-header">Create New Order</div>
        <form onSubmit={onCreate}>
          <div className="form-row">
            <div className="form-group">
              <label>Order Number *</label>
              <input value={orderNumber} onChange={e=>setOrderNumber(e.target.value)} placeholder="SO-2024-001" required />
            </div>
            <div className="form-group">
              <label>Contact</label>
              <select value={contactId || ''} onChange={e=>setContactId(e.target.value ? Number(e.target.value) : undefined)}>
                <option value="">Select a contact...</option>
                {contacts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Status</label>
              <select value={status} onChange={e=>setStatus(e.target.value)}>
                <option value="draft">Draft</option>
                <option value="confirmed">Confirmed</option>
                <option value="shipped">Shipped</option>
                <option value="invoiced">Invoiced</option>
              </select>
            </div>
            <div className="form-group">
              <label>Total Amount</label>
              <input value={total} onChange={e=>setTotal(e.target.value)} placeholder="1000.00" type="number" step="0.01" />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Create Order</button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">All Orders ({items.length})</div>
        {items.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Order Number</th>
                  <th>Contact ID</th>
                  <th>Status</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {items.map(o => (
                  <tr key={o.id}>
                    <td><strong>{o.order_number}</strong></td>
                    <td>{o.contact_id || '—'}</td>
                    <td>
                      <span className={`badge badge-${getStatusColor(o.status)}`}>
                        {o.status}
                      </span>
                    </td>
                    <td>${o.total.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">🛒</div>
            <p>No sales orders yet. Create your first order above.</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
