# WorkOS - Modern Business Operating System

![Status](https://img.shields.io/badge/status-production--ready-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Next.js](https://img.shields.io/badge/Next.js-14.2-black)
![Python](https://img.shields.io/badge/Python-3.11+-blue)

**WorkOS** is a modern, high-performance ERP system built to be better than Odoo. Features include CRM, sales orders, inventory, invoicing, project management, and comprehensive role-based access control.

## Features

### ✅ Complete Modules (7/7)
- **👥 Contacts (CRM)**: Customer and partner management
- **💼 Deals Pipeline**: Sales opportunity tracking
- **📦 Inventory**: Product and stock management with SKU tracking
- **🛒 Sales Orders**: Order processing and fulfillment
- **🧾 Invoicing**: Invoice generation linked to sales orders
- **🚀 Projects**: Project and task management with timesheets
- **📊 Dashboard**: Real-time analytics and activity feed

### 🔒 Enterprise Security
- **Password Hashing**: bcrypt with salt for all user credentials
- **JWT-like Tokens**: Signed tokens with 24h expiration
- **RBAC**: Role-based permissions (Admin, Sales, Viewer)
- **Auth Decorators**: `@require_auth` on all protected endpoints

### 🎨 Modern UI/UX (Better than Odoo)
- **Responsive Design**: Mobile-first with CSS variables
- **Card-Based Layout**: Clean, modern interface
- **Sidebar Navigation**: Easy access to all modules
- **Status Badges**: Color-coded for quick recognition
- **Empty States**: Helpful prompts when no data exists
- **Loading States**: Smooth UX with loading indicators

## Tech Stack

### Backend
- **FastAPI** 0.115: High-performance async Python framework
- **SQLAlchemy** 2.0: ORM with Alembic migrations
- **PostgreSQL** 16 (prod) / SQLite (dev)
- **bcrypt**: Password hashing
- **Uvicorn**: ASGI server

### Frontend
- **Next.js** 14.2: React framework with SSR
- **TypeScript** 5.6: Type-safe development
- **CSS Variables**: Modern theming system

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 16 (optional, uses SQLite by default)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations (creates tables)
alembic upgrade head

# Seed database with demo data
python -m app.seeds

# Start FastAPI server
uvicorn app.fastapi_main:app --host 127.0.0.1 --port 8000 --reload
```

Server runs at: **http://127.0.0.1:8000**

### Frontend Setup

```bash
cd admin

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:3000**

### Demo Credentials

| Username | Password   | Role   | Permissions           |
|----------|------------|--------|-----------------------|
| admin    | admin123   | Admin  | All permissions       |
| sales    | sales123   | Sales  | Read/Write (no delete)|
| viewer   | viewer123  | Viewer | Read-only access      |

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Key Endpoints

```
POST   /auth/login              # Authentication
GET    /contacts/               # List contacts
POST   /contacts/               # Create contact
GET    /deals/                  # List deals
POST   /deals/                  # Create deal
GET    /inventory/              # List products
POST   /inventory/              # Create product
GET    /sales/                  # List sales orders
POST   /sales/                  # Create order
GET    /invoices/               # List invoices
POST   /invoices/               # Create invoice
GET    /projects/               # List projects
POST   /projects/               # Create project
GET    /projects/{id}/tasks     # List tasks
POST   /projects/{id}/tasks     # Create task
```

All endpoints (except `/auth/login`) require `Authorization: Bearer <token>` header.

## Database Schema

### Core Tables
- `contact` - Customers and partners
- `deal` - Sales opportunities
- `product` - Inventory items
- `sale_order` + `order_item` - Sales orders
- `invoice` + `invoice_item` - Invoicing
- `project` + `task` + `time_sheet` - Project management

### Auth & RBAC
- `user` - User accounts with hashed passwords
- `role` - User roles (Admin, Sales, Viewer)
- `permission` - Granular permissions (14 total)
- `role_permission` - Role-to-permission mappings

## Development Roadmap

### 🎯 Phase 1: Enhanced Modules (Next Sprint - 2 weeks)
**Priority: High | Impact: Revenue-Critical**

1. **Accounting Module**
   - Chart of accounts (COA) management
   - Journal entries with double-entry bookkeeping
   - Financial reports (P&L, Balance Sheet, Cash Flow)
   - Bank reconciliation
   - Multi-currency support

2. **HR & Payroll**
   - Employee records and org chart
   - Attendance tracking and timesheet integration
   - Leave management (vacation, sick days)
   - Payroll calculation with tax rules
   - Expense reimbursement workflows

3. **Manufacturing (MRP)**
   - Bill of Materials (BOM) builder
   - Work orders and production scheduling
   - Inventory reservations
   - Quality control checkpoints
   - Scrap and waste tracking

4. **Purchase Orders**
   - Vendor/supplier management
   - Request for Quotations (RFQ)
   - Purchase order approval workflows
   - Goods receipt and quality inspection
   - Vendor invoicing integration

### 🚀 Phase 2: Advanced Features (4 weeks)
**Priority: High | Impact: User Experience**

1. **Email Integration**
   - Send invoices and quotes via email
   - Email templates with variables
   - Campaign tracking (opens, clicks)
   - SMTP/SendGrid integration
   - Inbox sync for support tickets

2. **File Attachments**
   - Upload documents (PDF, images, Excel)
   - Attach to contacts, projects, invoices
   - Cloud storage (S3/Azure Blob)
   - File versioning
   - OCR for invoice scanning

3. **Advanced Reporting**
   - Custom dashboard builder with drag-drop widgets
   - Pivot tables for multi-dimensional analysis
   - Export to Excel, PDF, CSV
   - Scheduled reports via email
   - KPI tracking and alerts

4. **Webhooks & Integrations**
   - Outgoing webhooks for real-time events
   - Zapier/Make integration
   - Slack notifications
   - QuickBooks/Xero sync
   - Shopify/WooCommerce connectors

5. **API Rate Limiting**
   - Token bucket throttling
   - Per-user quotas
   - API usage analytics
   - Premium tier with higher limits

### ⚡ Phase 3: Multi-Tenancy & Scale (6 weeks)
**Priority: Medium | Impact: Enterprise Sales**

1. **Multi-Company Architecture**
   - Database-per-tenant isolation
   - Subdomain routing (company1.workos.com)
   - Cross-company reporting (holding companies)
   - Data residency (EU/US/Asia)

2. **Advanced RBAC**
   - Field-level permissions (hide sensitive data)
   - Record rules (only see own records)
   - Department-based access control
   - Custom roles and permission sets

3. **Audit Logs**
   - Complete change history for all records
   - Who/what/when tracking
   - Compliance reports (SOC 2, GDPR)
   - Tamper-proof log storage

4. **Background Jobs**
   - Celery with Redis/RabbitMQ
   - Long-running report generation
   - Batch invoice sending
   - Scheduled data imports
   - Job monitoring dashboard

5. **Caching Layer**
   - Redis caching for frequent queries
   - HTTP cache headers
   - Dashboard metric pre-computation
   - Query result memoization

### 🏢 Phase 4: Enterprise Features (8 weeks)
**Priority: Low | Impact: Enterprise Contracts**

1. **SSO & Advanced Auth**
   - SAML 2.0 for enterprise SSO
   - OAuth 2.0 providers (Google, Microsoft)
   - Two-factor authentication (TOTP)
   - IP allowlisting
   - Session management

2. **Workflow Engine**
   - Visual workflow builder
   - Custom approval chains
   - Conditional logic and branching
   - Email/Slack notifications
   - SLA tracking

3. **Mobile Apps**
   - React Native iOS app
   - React Native Android app
   - Offline mode with sync
   - Push notifications
   - Barcode scanning for inventory

4. **AI Features**
   - Sales forecasting with ML
   - Inventory demand prediction
   - Chatbot support (RAG with company data)
   - Invoice OCR auto-filling
   - Anomaly detection in accounting

5. **GraphQL API**
   - Alternative to REST
   - Real-time subscriptions
   - Query optimization
   - Schema introspection
   - Apollo Client integration

### 🔧 Phase 5: DevOps & Production (Ongoing)
**Priority: Critical | Impact: Reliability**

1. **Containerization**
   - Multi-container Docker Compose
   - Kubernetes deployment manifests
   - Helm charts for easy deployment
   - Secret management (Vault)
   - Auto-scaling policies

2. **CI/CD Pipeline**
   - GitHub Actions for tests and linting
   - Automated deployments to staging/prod
   - Database migration automation
   - Rollback procedures
   - Canary deployments

3. **Monitoring & Observability**
   - Prometheus metrics
   - Grafana dashboards
   - Sentry error tracking
   - Structured logging (ELK stack)
   - Uptime monitoring (UptimeRobot)

4. **Performance Optimization**
   - Database query profiling
   - Index optimization
   - CDN for static assets (Cloudflare)
   - Lazy loading and pagination
   - Database connection pooling

5. **Security Hardening**
   - Regular dependency updates
   - Penetration testing
   - OWASP Top 10 compliance
   - Rate limiting and DDoS protection
   - Automated security scans

## Project Structure

```
project003/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routers (CURRENT)
│   │   │   ├── contacts.py
│   │   │   ├── deals.py
│   │   │   ├── inventory.py
│   │   │   ├── sales.py
│   │   │   ├── invoices.py
│   │   │   └── projects.py
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── contact.py
│   │   │   ├── deal.py
│   │   │   ├── product.py
│   │   │   ├── sale_order.py
│   │   │   ├── invoice.py
│   │   │   ├── project.py
│   │   │   ├── user.py
│   │   │   └── permission.py
│   │   ├── routes/           # Flask routes (DEPRECATED)
│   │   ├── fastapi_auth.py   # Auth dependencies
│   │   ├── fastapi_main.py   # FastAPI app ⭐
│   │   ├── db.py             # Database setup
│   │   ├── utils.py          # Password hashing
│   │   └── seeds.py          # Database seeding
│   ├── alembic/              # Database migrations
│   │   └── versions/
│   │       ├── 0001_init.py
│   │       ├── 0002_inventory_sales.py
│   │       └── 0003_permissions_invoicing_projects.py
│   └── requirements.txt
│
└── admin/                    # Next.js frontend
    ├── components/
    │   └── Layout.tsx        # Shared layout with sidebar
    ├── pages/
    │   ├── index.tsx         # Login page
    │   ├── dashboard.tsx     # Main dashboard ⭐
    │   ├── contacts.tsx
    │   ├── deals.tsx
    │   ├── inventory.tsx
    │   ├── sales.tsx
    │   ├── invoices.tsx
    │   └── projects.tsx
    ├── lib/
    │   └── api.ts            # API client
    └── styles.css            # Modern design system
```

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend type checking
cd admin
npm run type-check
```

## Deployment

### Backend (FastAPI)

**Development**
```bash
uvicorn app.fastapi_main:app --reload
```

**Production with Gunicorn**
```bash
gunicorn app.fastapi_main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Frontend (Next.js)

```bash
cd admin
npm run build
npm start
```

### Environment Variables

**backend/.env**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/workos
SECRET_KEY=your-secret-key-change-in-production
```

**admin/.env.local**
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built to be **better than Odoo** with modern tech stack
- FastAPI for performance, Next.js for modern UX
- Inspired by enterprise ERP systems but designed for simplicity and speed

---

**WorkOS** - *Your business, optimized.* ⚡

Repository: https://github.com/kellyworkos00-droid/project003
