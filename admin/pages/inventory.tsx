import Layout from '../components/Layout'
import { FormEvent, useEffect, useState } from 'react'
import { api } from '../lib/api'

type Product = { id: number; name: string; sku: string; description?: string; price: number; stock: number }

export default function InventoryPage() {
  const [items, setItems] = useState<Product[]>([])
  const [name, setName] = useState('')
  const [sku, setSku] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('0')
  const [stock, setStock] = useState('0')

  async function load() {
    const data = await api('/inventory/')
    setItems(data)
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault()
    await api('/inventory/', {
      method: 'POST',
      body: JSON.stringify({
        name,
        sku,
        description: description || null,
        price: parseFloat(price),
        stock: parseInt(stock, 10),
      }),
    })
    setName(''); setSku(''); setDescription(''); setPrice('0'); setStock('0');
    await load()
  }

  useEffect(() => { load() }, [])

  const getStockStatus = (stock: number) => {
    if (stock === 0) return { label: 'Out of Stock', color: 'danger' }
    if (stock < 10) return { label: 'Low Stock', color: 'warning' }
    return { label: 'In Stock', color: 'success' }
  }

  return (
    <Layout title="Inventory" subtitle="Manage products and stock levels">
      <div className="card">
        <div className="card-header">Add New Product</div>
        <form onSubmit={onCreate}>
          <div className="form-row">
            <div className="form-group">
              <label>Product Name *</label>
              <input value={name} onChange={e=>setName(e.target.value)} placeholder="Awesome Widget" required />
            </div>
            <div className="form-group">
              <label>SKU *</label>
              <input value={sku} onChange={e=>setSku(e.target.value)} placeholder="WIDGET-001" required />
            </div>
          </div>
          <div className="form-group">
            <label>Description</label>
            <input value={description} onChange={e=>setDescription(e.target.value)} placeholder="Optional product description" />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Price</label>
              <input value={price} onChange={e=>setPrice(e.target.value)} placeholder="99.99" type="number" step="0.01" />
            </div>
            <div className="form-group">
              <label>Stock Quantity</label>
              <input value={stock} onChange={e=>setStock(e.target.value)} placeholder="100" type="number" />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Add Product</button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">All Products ({items.length})</div>
        {items.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Name</th>
                  <th>Price</th>
                  <th>Stock</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {items.map(p => {
                  const stockStatus = getStockStatus(p.stock)
                  return (
                    <tr key={p.id}>
                      <td><code>{p.sku}</code></td>
                      <td><strong>{p.name}</strong></td>
                      <td>${p.price.toFixed(2)}</td>
                      <td>{p.stock}</td>
                      <td>
                        <span className={`badge badge-${stockStatus.color}`}>
                          {stockStatus.label}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">📦</div>
            <p>No products yet. Add your first product above.</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
