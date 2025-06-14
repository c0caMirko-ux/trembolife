from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ORM import Base  # ORM con tus modelos
from Datos import agregar_datos  # Datos de prueba


def create_database(admin_url: str, dbname: str) -> None:
    """Crea la base de datos si no existe."""
    engine = create_engine(admin_url)
    with engine.connect() as conn:
        try:
            conn.execution_options(isolation_level="AUTOCOMMIT") \
                .execute(text(f'CREATE DATABASE "{dbname}"'))  # Protege el nombre
            print(f"✅ Base de datos '{dbname}' creada.")
        except ProgrammingError:
            print(f"⚠️ Base de datos '{dbname}' ya existe o no se pudo crear.")
    engine.dispose()


def get_engine(db_url: str) -> Engine:
    """Devuelve un engine SQLAlchemy desde una URL."""
    return create_engine(db_url)


def create_schema(engine: Engine) -> None:
    """Crea las tablas según el ORM."""
    Base.metadata.create_all(engine)
    print("✅ Tablas creadas correctamente.")


def main():
    # Configura tus datos de conexión
    ADMIN_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
    DB_NAME = "suplementos_store"
    DB_URL = f"postgresql+psycopg2://postgres:123456@localhost:5432/{DB_NAME}"

    # 1. Crear la base si no existe
    create_database(ADMIN_URL, DB_NAME)

    # 2. Crear engine y esquema
    engine = get_engine(DB_URL)
    create_schema(engine)

    # 3. Insertar datos iniciales
    Session = sessionmaker(bind=engine)
    session = Session()
    agregar_datos(session)

    print("🎉 Migración completa: base, tablas y datos insertados.")


if __name__ == "__main__":
    main()
