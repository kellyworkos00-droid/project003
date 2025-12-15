import Link from 'next/link'
import { useRouter } from 'next/router'
import { ReactNode, useEffect, useState } from 'react'
import { getToken } from '../lib/api'

interface LayoutProps {
  children: ReactNode
  title?: string
  subtitle?: string
}

export default function Layout({ children, title, subtitle }: LayoutProps) {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const token = getToken()
    if (!token && router.pathname !== '/') {
      router.push('/')
    }
    // Optionally decode token to get user info
  }, [router])

  const navItems = [
    { href: '/dashboard', label: '📊 Dashboard', icon: '📊' },
    { href: '/contacts', label: '👥 Contacts', icon: '👥' },
    { href: '/deals', label: '💼 Deals', icon: '💼' },
    { href: '/sales', label: '🛒 Sales Orders', icon: '🛒' },
    { href: '/invoices', label: '🧾 Invoices', icon: '🧾' },
    { href: '/inventory', label: '📦 Inventory', icon: '📦' },
    { href: '/projects', label: '🚀 Projects', icon: '🚀' },
  ]

  const isActive = (path: string) => router.pathname === path

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          ⚡ OpenERP
        </div>
        <ul className="sidebar-nav">
          {navItems.map(item => (
            <li key={item.href}>
              <Link href={item.href} className={isActive(item.href) ? 'active' : ''}>
                <span style={{marginRight: '8px'}}>{item.icon}</span>
                {item.label.replace(/^.+ /, '')}
              </Link>
            </li>
          ))}
        </ul>
      </aside>
      <main className="main-content">
        {title && (
          <div className="page-header">
            <h1 className="page-title">{title}</h1>
            {subtitle && <p className="page-subtitle">{subtitle}</p>}
          </div>
        )}
        {children}
      </main>
    </div>
  )
}
