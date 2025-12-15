import Layout from '../components/Layout'
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

  const getStageColor = (stage?: string) => {
    switch (stage) {
      case 'qualified': return 'success'
      case 'proposal': return 'warning'
      case 'won': return 'success'
      case 'lost': return 'danger'
      default: return 'info'
    }
  }

  return (
    <Layout title="Deals Pipeline" subtitle="Track and manage your sales opportunities">
      <div className="card">
        <div className="card-header">Create New Deal</div>
        <form onSubmit={onCreate}>
          <div className="form-row">
            <div className="form-group">
              <label>Title *</label>
              <input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Big Enterprise Deal" required />
            </div>
            <div className="form-group">
              <label>Amount</label>
              <input value={amount} onChange={e=>setAmount(e.target.value)} placeholder="50000" type="number" step="0.01" />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Stage</label>
              <select value={stage} onChange={e=>setStage(e.target.value)}>
                <option value="new">New</option>
                <option value="qualified">Qualified</option>
                <option value="proposal">Proposal</option>
                <option value="won">Won</option>
                <option value="lost">Lost</option>
              </select>
            </div>
            <div className="form-group">
              <label>Contact</label>
              <select value={contactId || ''} onChange={e=>setContactId(e.target.value ? Number(e.target.value) : undefined)}>
                <option value="">Select a contact...</option>
                {contacts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Create Deal</button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">All Deals ({items.length})</div>
        {items.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Amount</th>
                  <th>Stage</th>
                  <th>Contact ID</th>
                </tr>
              </thead>
              <tbody>
                {items.map(d => (
                  <tr key={d.id}>
                    <td><strong>{d.title}</strong></td>
                    <td>${d.amount.toLocaleString()}</td>
                    <td>
                      <span className={`badge badge-${getStageColor(d.stage)}`}>
                        {d.stage || 'new'}
                      </span>
                    </td>
                    <td>{d.contact_id || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">💼</div>
            <p>No deals yet. Create your first opportunity above.</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
