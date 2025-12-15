import sys
from pathlib import Path
from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Add backend path so `app` package is importable when running alembic from backend/
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

config = context.config

# Read DATABASE_URL from env, fallback to SQLite
db_url = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.db import Base  # noqa: E402

# target metadata for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
