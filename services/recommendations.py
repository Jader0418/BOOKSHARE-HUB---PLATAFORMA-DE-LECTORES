from sqlmodel import Session, select
from models import BookRecommendation, Friendship


def obtener_todas(session: Session):
    """Retorna todas las recomendaciones públicas."""
    return session.exec(
        select(BookRecommendation).where(BookRecommendation.visibility == "PUBLIC")
    ).all()


def obtener_por_id(session: Session, rec_id: int):
    """Retorna una recomendación por su id."""
    return session.get(BookRecommendation, rec_id)


def obtener_visibles(session: Session, viewer_id: int):
    """
    Retorna recomendaciones según visibilidad:
    - PUBLIC: visible para todos
    - PRIVATE: solo para el autor
    - FRIENDS: solo para amigos aceptados
    """
    recomendaciones = session.exec(select(BookRecommendation)).all()
    visibles = []

    for rec in recomendaciones:
        # PUBLIC - visible para todos
        if rec.visibility == "PUBLIC":
            visibles.append(rec)

        # PRIVATE - solo el autor
        elif rec.visibility == "PRIVATE" and rec.user_id == viewer_id:
            visibles.append(rec)

        # FRIENDS - solo amigos aceptados
        elif rec.visibility == "FRIENDS":
            if rec.user_id == viewer_id:
                visibles.append(rec)
            else:
                amistad = session.exec(
                    select(Friendship).where(
                        ((Friendship.requester_id == viewer_id) & (Friendship.receiver_id == rec.user_id)) |
                        ((Friendship.requester_id == rec.user_id) & (Friendship.receiver_id == viewer_id))
                    )
                ).first()
                if amistad and amistad.status == "ACCEPTED":
                    visibles.append(rec)

    return visibles


def crear(session: Session, recomendacion: BookRecommendation):
    """Crea una nueva recomendación."""
    session.add(recomendacion)
    session.commit()
    session.refresh(recomendacion)
    return recomendacion


def actualizar(session: Session, rec_id: int, datos: BookRecommendation):
    """Actualiza una recomendación existente."""
    rec = session.get(BookRecommendation, rec_id)
    if not rec:
        return None
    rec.status = datos.status
    rec.rating = datos.rating
    rec.short_review = datos.short_review
    rec.visibility = datos.visibility
    session.commit()
    session.refresh(rec)
    return rec


def eliminar(session: Session, rec_id: int):
    """Elimina una recomendación por su id."""
    rec = session.get(BookRecommendation, rec_id)
    if not rec:
        return None
    session.delete(rec)
    session.commit()
    return {"mensaje": "Recomendación eliminada"}
