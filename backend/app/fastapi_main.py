from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.db import Base, engine
from app.api.contacts import router as contacts_router
from app.api.deals import router as deals_router
from app.api.inventory import router as inventory_router
from app.api.sales import router as sales_router
from app.api.invoices import router as invoices_router
from app.api.projects import router as projects_router
from app.fastapi_auth import router as auth_router

# Ensure data dir exists for SQLite development
Path("data").mkdir(parents=True, exist_ok=True)

# Create tables (dev convenience)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WorkOS API", version="1.0.0", description="Modern business operating system - better than Odoo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(deals_router, prefix="/deals", tags=["deals"])
app.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])
app.include_router(invoices_router, prefix="/invoices", tags=["invoices"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])


@app.get("/")
async def health():
    return {"app": "WorkOS", "version": "1.0.0", "status": "ok"}
