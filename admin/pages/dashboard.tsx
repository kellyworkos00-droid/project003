import Layout from '../components/Layout'
import { useEffect, useState } from 'react'
import { api } from '../lib/api'

export default function DashboardPage() {
  const [stats, setStats] = useState({
    contacts: 0,
    deals: 0,
    products: 0,
    orders: 0,
    invoices: 0,
    projects: 0,
  })
  const [recentActivity, setRecentActivity] = useState<any[]>([])

  useEffect(() => {
    loadDashboard()
  }, [])

  async function loadDashboard() {
    try {
      const [contacts, deals, products, orders, invoices, projects] = await Promise.all([
        api('/contacts/').catch(() => []),
        api('/deals/').catch(() => []),
        api('/inventory/').catch(() => []),
        api('/sales/').catch(() => []),
        api('/invoices/').catch(() => []),
        api('/projects/').catch(() => []),
      ])
      setStats({
        contacts: contacts.length,
        deals: deals.length,
        products: products.length,
        orders: orders.length,
        invoices: invoices.length,
        projects: projects.length,
      })
      
      // Recent activity (last 5 deals)
      setRecentActivity(deals.slice(0, 5))
    } catch (err) {
      console.error('Failed to load dashboard', err)
    }
  }

  return (
    <Layout title="Dashboard" subtitle="Welcome back! Here's what's happening.">
      <div className="stats-grid">
        <div className="stat-card" style={{borderLeftColor: '#7c3aed'}}>
          <div className="stat-label">👥 Total Contacts</div>
          <div className="stat-value">{stats.contacts}</div>
        </div>
        <div className="stat-card" style={{borderLeftColor: '#10b981'}}>
          <div className="stat-label">💼 Active Deals</div>
          <div className="stat-value">{stats.deals}</div>
        </div>
        <div className="stat-card" style={{borderLeftColor: '#f59e0b'}}>
          <div className="stat-label">🛒 Sales Orders</div>
          <div className="stat-value">{stats.orders}</div>
        </div>
        <div className="stat-card" style={{borderLeftColor: '#ef4444'}}>
          <div className="stat-label">🧾 Invoices</div>
          <div className="stat-value">{stats.invoices}</div>
        </div>
        <div className="stat-card" style={{borderLeftColor: '#8b5cf6'}}>
          <div className="stat-label">📦 Products</div>
          <div className="stat-value">{stats.products}</div>
        </div>
        <div className="stat-card" style={{borderLeftColor: '#06b6d4'}}>
          <div className="stat-label">🚀 Projects</div>
          <div className="stat-value">{stats.projects}</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">Recent Deals</div>
        {recentActivity.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Amount</th>
                  <th>Stage</th>
                </tr>
              </thead>
              <tbody>
                {recentActivity.map(deal => (
                  <tr key={deal.id}>
                    <td>{deal.title}</td>
                    <td>${deal.amount}</td>
                    <td>
                      <span className={`badge badge-${deal.stage === 'qualified' ? 'success' : 'info'}`}>
                        {deal.stage}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">📊</div>
            <p>No recent deals to display</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
