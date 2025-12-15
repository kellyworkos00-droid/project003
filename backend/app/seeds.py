"""
Seed script to populate initial roles, users, and sample data.
Run: python -m app.seeds
"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db import SessionLocal, Base, engine
from app.models.user import User, Role
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.product import Product
from app.models.sale_order import SaleOrder, OrderItem
from app.models.permission import Permission, RolePermission
from app.utils import hash_password


def seed():
    # Create tables if needed (dev mode)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Seed roles
        if not db.query(Role).filter_by(name="admin").first():
            roles = [
                Role(name="admin", description="Full system access"),
                Role(name="sales", description="Sales and CRM access"),
                Role(name="viewer", description="Read-only access"),
            ]
            db.add_all(roles)
            db.commit()
            print("✓ Seeded roles: admin, sales, viewer")

        # Seed users
        admin_role = db.query(Role).filter_by(name="admin").first()
        sales_role = db.query(Role).filter_by(name="sales").first()
        viewer_role = db.query(Role).filter_by(name="viewer").first()

        if not db.query(User).filter_by(username="admin").first():
            users = [
                User(username="admin", email="admin@openerp.local", 
                     password_hash=hash_password("admin123"), role_id=admin_role.id, is_active=1),
                User(username="sales", email="sales@openerp.local", 
                     password_hash=hash_password("sales123"), role_id=sales_role.id, is_active=1),
                User(username="viewer", email="viewer@openerp.local", 
                     password_hash=hash_password("viewer123"), role_id=viewer_role.id, is_active=1),
            ]
            db.add_all(users)
            db.commit()
            print("✓ Seeded users: admin (admin123), sales (sales123), viewer (viewer123)")

        # Seed permissions
        if db.query(Permission).count() == 0:
            permissions = [
                # Contacts
                Permission(name="contacts.read", description="View contacts"),
                Permission(name="contacts.write", description="Create/edit contacts"),
                Permission(name="contacts.delete", description="Delete contacts"),
                # Deals
                Permission(name="deals.read", description="View deals"),
                Permission(name="deals.write", description="Create/edit deals"),
                Permission(name="deals.delete", description="Delete deals"),
                # Inventory
                Permission(name="inventory.read", description="View products"),
                Permission(name="inventory.write", description="Create/edit products"),
                Permission(name="inventory.delete", description="Delete products"),
                # Sales
                Permission(name="sales.read", description="View sales orders"),
                Permission(name="sales.write", description="Create/edit sales orders"),
                Permission(name="sales.delete", description="Delete sales orders"),
                # Admin
                Permission(name="users.manage", description="Manage users"),
                Permission(name="settings.manage", description="Manage settings"),
            ]
            db.add_all(permissions)
            db.commit()
            print("✓ Seeded 14 permissions")

            # Assign all permissions to admin role
            all_perms = db.query(Permission).all()
            for perm in all_perms:
                db.add(RolePermission(role_id=admin_role.id, permission_id=perm.id))
            
            # Assign read/write permissions to sales role (not delete or admin)
            sales_perms = [p for p in all_perms if p.name.endswith('.read') or p.name.endswith('.write')]
            for perm in sales_perms:
                db.add(RolePermission(role_id=sales_role.id, permission_id=perm.id))
            
            # Assign only read permissions to viewer role
            viewer_perms = [p for p in all_perms if p.name.endswith('.read')]
            for perm in viewer_perms:
                db.add(RolePermission(role_id=viewer_role.id, permission_id=perm.id))
            
            db.commit()
            print("✓ Assigned permissions to roles")

        # Seed contacts
        if db.query(Contact).count() == 0:
            contacts = [
                Contact(name="Acme Corp", email="contact@acme.com", phone="+1-555-0100", company="Acme Corp"),
                Contact(name="Jane Doe", email="jane@example.com", phone="+1-555-0101", company="ABC Inc"),
                Contact(name="John Smith", email="john@example.com", phone="+1-555-0102", company="XYZ Ltd"),
            ]
            db.add_all(contacts)
            db.commit()
            print("✓ Seeded 3 contacts")

        # Seed products
        if db.query(Product).count() == 0:
            products = [
                Product(name="Widget A", sku="WGT-001", description="Premium widget", price=29.99, stock=100),
                Product(name="Widget B", sku="WGT-002", description="Standard widget", price=19.99, stock=200),
                Product(name="Gadget X", sku="GDG-001", description="Advanced gadget", price=99.99, stock=50),
            ]
            db.add_all(products)
            db.commit()
            print("✓ Seeded 3 products")

        # Seed deals
        if db.query(Deal).count() == 0:
            contact = db.query(Contact).first()
            deals = [
                Deal(title="Enterprise Deal", amount=50000, stage="qualified", contact_id=contact.id if contact else None),
                Deal(title="SMB Opportunity", amount=5000, stage="proposal", contact_id=contact.id if contact else None),
            ]
            db.add_all(deals)
            db.commit()
            print("✓ Seeded 2 deals")

        # Seed sale orders
        if db.query(SaleOrder).count() == 0:
            contact = db.query(Contact).first()
            product = db.query(Product).first()
            order = SaleOrder(order_number="SO-001", contact_id=contact.id if contact else None, status="confirmed", total=299.90)
            db.add(order)
            db.commit()

            if product:
                item = OrderItem(order_id=order.id, product_id=product.id, quantity=10, unit_price=29.99, subtotal=299.90)
                db.add(item)
                db.commit()
            print("✓ Seeded 1 sale order with items")

        print("\n✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
