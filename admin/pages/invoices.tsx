import Layout from '../components/Layout'
import { FormEvent, useEffect, useState } from 'react'
import { api } from '../lib/api'

type Invoice = {
  id: number
  invoice_number: string
  sale_order_id?: number
  contact_id?: number
  status: string
  subtotal: number
  tax: number
  total: number
  issue_date: string
  due_date?: string
}

type SaleOrder = { id: number; order_number: string }
type Contact = { id: number; name: string }

export default function InvoicesPage() {
  const [items, setItems] = useState<Invoice[]>([])
  const [saleOrders, setSaleOrders] = useState<SaleOrder[]>([])
  const [contacts, setContacts] = useState<Contact[]>([])
  const [invoiceNumber, setInvoiceNumber] = useState('')
  const [saleOrderId, setSaleOrderId] = useState<number | undefined>()
  const [contactId, setContactId] = useState<number | undefined>()
  const [status, setStatus] = useState('draft')
  const [subtotal, setSubtotal] = useState('0')
  const [tax, setTax] = useState('0')
  const [issueDate, setIssueDate] = useState('')
  const [dueDate, setDueDate] = useState('')

  async function load() {
    const [invoices, orders, cs] = await Promise.all([
      api('/invoices/').catch(() => []),
      api('/sales/').catch(() => []),
      api('/contacts/').catch(() => []),
    ])
    setItems(invoices)
    setSaleOrders(orders)
    setContacts(cs)
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault()
    const sub = parseFloat(subtotal)
    const t = parseFloat(tax)
    await api('/invoices/', {
      method: 'POST',
      body: JSON.stringify({
        invoice_number: invoiceNumber,
        sale_order_id: saleOrderId,
        contact_id: contactId,
        status,
        subtotal: sub,
        tax: t,
        total: sub + t,
        issue_date: issueDate,
        due_date: dueDate || null,
      }),
    })
    setInvoiceNumber('')
    setSaleOrderId(undefined)
    setContactId(undefined)
    setStatus('draft')
    setSubtotal('0')
    setTax('0')
    setIssueDate('')
    setDueDate('')
    await load()
  }

  useEffect(() => { load() }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'secondary'
      case 'sent': return 'info'
      case 'paid': return 'success'
      case 'overdue': return 'danger'
      case 'cancelled': return 'secondary'
      default: return 'secondary'
    }
  }

  return (
    <Layout title="Invoices" subtitle="Manage customer invoices and billing">
      <div className="card">
        <div className="card-header">Create New Invoice</div>
        <form onSubmit={onCreate}>
          <div className="form-row">
            <div className="form-group">
              <label>Invoice Number *</label>
              <input
                value={invoiceNumber}
                onChange={e=>setInvoiceNumber(e.target.value)}
                placeholder="INV-2024-001"
                required
              />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select value={status} onChange={e=>setStatus(e.target.value)}>
                <option value="draft">Draft</option>
                <option value="sent">Sent</option>
                <option value="paid">Paid</option>
                <option value="overdue">Overdue</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Sale Order</label>
              <select value={saleOrderId || ''} onChange={e=>setSaleOrderId(e.target.value ? Number(e.target.value) : undefined)}>
                <option value="">Select sale order...</option>
                {saleOrders.map(o => <option key={o.id} value={o.id}>{o.order_number}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Contact</label>
              <select value={contactId || ''} onChange={e=>setContactId(e.target.value ? Number(e.target.value) : undefined)}>
                <option value="">Select contact...</option>
                {contacts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Subtotal</label>
              <input
                type="number"
                step="0.01"
                value={subtotal}
                onChange={e=>setSubtotal(e.target.value)}
                placeholder="1000.00"
              />
            </div>
            <div className="form-group">
              <label>Tax</label>
              <input
                type="number"
                step="0.01"
                value={tax}
                onChange={e=>setTax(e.target.value)}
                placeholder="100.00"
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Issue Date *</label>
              <input
                type="date"
                value={issueDate}
                onChange={e=>setIssueDate(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Due Date</label>
              <input
                type="date"
                value={dueDate}
                onChange={e=>setDueDate(e.target.value)}
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Create Invoice</button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">All Invoices ({items.length})</div>
        {items.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Invoice #</th>
                  <th>Issue Date</th>
                  <th>Due Date</th>
                  <th>Total</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {items.map(inv => (
                  <tr key={inv.id}>
                    <td><strong>{inv.invoice_number}</strong></td>
                    <td>{inv.issue_date}</td>
                    <td>{inv.due_date || '—'}</td>
                    <td>${inv.total.toLocaleString()}</td>
                    <td>
                      <span className={`badge badge-${getStatusColor(inv.status)}`}>
                        {inv.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">🧾</div>
            <p>No invoices yet. Create your first invoice above.</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
