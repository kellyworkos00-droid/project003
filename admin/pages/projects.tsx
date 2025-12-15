import Layout from '../components/Layout'
import { FormEvent, useEffect, useState } from 'react'
import { api } from '../lib/api'

type Project = {
  id: number
  name: string
  code: string
  description?: string
  contact_id?: number
  status: string
  start_date?: string
  end_date?: string
}

type Contact = { id: number; name: string }

export default function ProjectsPage() {
  const [items, setItems] = useState<Project[]>([])
  const [contacts, setContacts] = useState<Contact[]>([])
  const [name, setName] = useState('')
  const [code, setCode] = useState('')
  const [description, setDescription] = useState('')
  const [contactId, setContactId] = useState<number | undefined>()
  const [status, setStatus] = useState('planning')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  async function load() {
    const [projects, cs] = await Promise.all([
      api('/projects/').catch(() => []),
      api('/contacts/').catch(() => []),
    ])
    setItems(projects)
    setContacts(cs)
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault()
    await api('/projects/', {
      method: 'POST',
      body: JSON.stringify({
        name,
        code,
        description: description || null,
        contact_id: contactId,
        status,
        start_date: startDate || null,
        end_date: endDate || null,
      }),
    })
    setName('')
    setCode('')
    setDescription('')
    setContactId(undefined)
    setStatus('planning')
    setStartDate('')
    setEndDate('')
    await load()
  }

  useEffect(() => { load() }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'planning': return 'secondary'
      case 'active': return 'info'
      case 'on_hold': return 'warning'
      case 'completed': return 'success'
      case 'cancelled': return 'danger'
      default: return 'secondary'
    }
  }

  return (
    <Layout title="Projects" subtitle="Track project timelines and deliverables">
      <div className="card">
        <div className="card-header">Create New Project</div>
        <form onSubmit={onCreate}>
          <div className="form-row">
            <div className="form-group">
              <label>Project Name *</label>
              <input
                value={name}
                onChange={e=>setName(e.target.value)}
                placeholder="Website Redesign"
                required
              />
            </div>
            <div className="form-group">
              <label>Project Code *</label>
              <input
                value={code}
                onChange={e=>setCode(e.target.value)}
                placeholder="PROJ-2024-001"
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label>Description</label>
            <input
              value={description}
              onChange={e=>setDescription(e.target.value)}
              placeholder="Project overview and goals"
            />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Status</label>
              <select value={status} onChange={e=>setStatus(e.target.value)}>
                <option value="planning">Planning</option>
                <option value="active">Active</option>
                <option value="on_hold">On Hold</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div className="form-group">
              <label>Client</label>
              <select value={contactId || ''} onChange={e=>setContactId(e.target.value ? Number(e.target.value) : undefined)}>
                <option value="">Select client...</option>
                {contacts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={e=>setStartDate(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={e=>setEndDate(e.target.value)}
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Create Project</button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">All Projects ({items.length})</div>
        {items.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Client</th>
                  <th>Status</th>
                  <th>Dates</th>
                </tr>
              </thead>
              <tbody>
                {items.map(p => (
                  <tr key={p.id}>
                    <td><code>{p.code}</code></td>
                    <td><strong>{p.name}</strong></td>
                    <td>{p.contact_id || '—'}</td>
                    <td>
                      <span className={`badge badge-${getStatusColor(p.status)}`}>
                        {p.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td>
                      {p.start_date && p.end_date 
                        ? `${p.start_date} → ${p.end_date}`
                        : p.start_date || '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">🚀</div>
            <p>No projects yet. Create your first project above.</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
