import Link from 'next/link'
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

  return (
    <div className="container">
      <h1>Inventory (Products)</h1>
      <nav>
        <Link href="/">Login</Link>
        <Link href="/contacts">Contacts</Link>
        <Link href="/deals">Deals</Link>
        <Link href="/sales">Sales Orders</Link>
      </nav>
      <form onSubmit={onCreate}>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Name" required />
        <input value={sku} onChange={e=>setSku(e.target.value)} placeholder="SKU" required />
        <input value={description} onChange={e=>setDescription(e.target.value)} placeholder="Description" />
        <input value={price} onChange={e=>setPrice(e.target.value)} placeholder="Price" type="number" step="0.01" />
        <input value={stock} onChange={e=>setStock(e.target.value)} placeholder="Stock" type="number" />
        <button type="submit">Create</button>
      </form>
      <table>
        <thead>
          <tr><th>ID</th><th>SKU</th><th>Name</th><th>Price</th><th>Stock</th></tr>
        </thead>
        <tbody>
          {items.map(p => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.sku}</td>
              <td>{p.name}</td>
              <td>${p.price}</td>
              <td>{p.stock}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
