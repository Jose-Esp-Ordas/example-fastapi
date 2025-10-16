from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from alembic import context
from dotenv import load_dotenv

# 📌 Cargar variables de entorno
load_dotenv()  # Asegúrate que .env está en la raíz del proyecto

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL no está definida en .env")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Reemplaza la URL de SQLAlchemy en alembic.ini con la de tu .env
config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Importa tus modelos aquí para autogenerate
target_metadata = SQLModel.metadata

# -------------------------
# Funciones para migración
# -------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Ejecutar migraciones según el modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
