# Import SQLAlchemy models here so Base.metadata sees them for table creation
from app.db.base_class import Base

# Contacts module
from app.modules.contacts.models import Contact  # noqa: F401
