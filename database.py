from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

# ─── CONFIGURACIÓN BASE DE DATOS ─────────────────────────────────────────────
sqlite_file_name = "bookshare.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    """Crea todas las tablas en la base de datos."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Genera una sesión de base de datos por cada petición."""
    with Session(engine) as session:
        yield session

# SessionDep es el tipo que usamos en las rutas para recibir la sesión
SessionDep = Annotated[Session, Depends(get_session)]
