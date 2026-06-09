from sqlmodel import Session, select
from models import Friendship


def obtener_todas(session: Session):
    """Retorna todas las amistades."""
    return session.exec(select(Friendship)).all()


def obtener_por_id(session: Session, friendship_id: int):
    """Retorna una amistad por su id."""
    return session.get(Friendship, friendship_id)


def crear(session: Session, amistad: Friendship):
    """
    Crea una solicitud de amistad.
    Verifica que no exista ya una relación entre los mismos usuarios.
    """
    existente = session.exec(
        select(Friendship).where(
            ((Friendship.requester_id == amistad.requester_id) & (Friendship.receiver_id == amistad.receiver_id)) |
            ((Friendship.requester_id == amistad.receiver_id) & (Friendship.receiver_id == amistad.requester_id))
        )
    ).first()

    if existente:
        return None  # ya existe relación

    session.add(amistad)
    session.commit()
    session.refresh(amistad)
    return amistad


def actualizar_estado(session: Session, friendship_id: int, nuevo_estado: str):
    """Actualiza el estado de una amistad (ACCEPTED, REJECTED, BLOCKED)."""
    amistad = session.get(Friendship, friendship_id)
    if not amistad:
        return None
    amistad.status = nuevo_estado
    session.commit()
    session.refresh(amistad)
    return amistad


def eliminar(session: Session, friendship_id: int):
    """Elimina una amistad por su id."""
    amistad = session.get(Friendship, friendship_id)
    if not amistad:
        return None
    session.delete(amistad)
    session.commit()
    return {"mensaje": "Amistad eliminada"}
