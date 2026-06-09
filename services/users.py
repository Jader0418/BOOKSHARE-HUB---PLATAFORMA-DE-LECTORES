from sqlmodel import Session, select
from models import User


def obtener_todos(session: Session):
    """Retorna todos los usuarios."""
    return session.exec(select(User)).all()


def obtener_por_id(session: Session, user_id: int):
    """Retorna un usuario por su id."""
    return session.get(User, user_id)


def crear(session: Session, usuario: User):
    """Crea un nuevo usuario."""
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def actualizar(session: Session, user_id: int, datos: User):
    """Actualiza un usuario existente."""
    usuario = session.get(User, user_id)
    if not usuario:
        return None
    usuario.username = datos.username
    usuario.email = datos.email
    usuario.full_name = datos.full_name
    usuario.is_active = datos.is_active
    session.commit()
    session.refresh(usuario)
    return usuario


def eliminar(session: Session, user_id: int):
    """Elimina un usuario por su id."""
    usuario = session.get(User, user_id)
    if not usuario:
        return None
    session.delete(usuario)
    session.commit()
    return {"mensaje": "Usuario eliminado"}
