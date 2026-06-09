from sqlmodel import Session, select
from fastapi import HTTPException
from models import (
    User, Book, BookRecommendation,
    ReadingListItem, Comment, Tag, BookTag, Friendship
)
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# SERVICIOS DE USUARIO
# ─────────────────────────────────────────────────────────────────────────────

def obtener_usuarios(session: Session):
    return session.exec(select(User)).all()

def obtener_usuario(user_id: int, session: Session):
    usuario = session.get(User, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

def crear_usuario(usuario: User, session: Session):
    # Verifica que no exista el mismo username
    existente = session.exec(select(User).where(User.username == usuario.username)).first()
    if existente:
        raise HTTPException(status_code=400, detail="El username ya existe")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def actualizar_usuario(user_id: int, datos: User, session: Session):
    usuario = session.get(User, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.full_name = datos.full_name
    usuario.email = datos.email
    usuario.is_active = datos.is_active
    session.commit()
    session.refresh(usuario)
    return usuario

def eliminar_usuario(user_id: int, session: Session):
    usuario = session.get(User, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return {"mensaje": "Usuario eliminado"}


# ─────────────────────────────────────────────────────────────────────────────
# SERVICIOS DE LIBRO
# ─────────────────────────────────────────────────────────────────────────────

def obtener_libros(session: Session):
    return session.exec(select(Book)).all()

def obtener_libro(book_id: int, session: Session):
    libro = session.get(Book, book_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

def crear_libro(libro: Book, session: Session):
    existente = session.exec(select(Book).where(Book.isbn == libro.isbn)).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un libro con ese ISBN")
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

def eliminar_libro(book_id: int, session: Session):
    libro = session.get(Book, book_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(libro)
    session.commit()
    return {"mensaje": "Libro eliminado"}


# ─────────────────────────────────────────────────────────────────────────────
# SERVICIOS DE RECOMENDACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def obtener_recomendaciones_publicas(session: Session):
    """Solo devuelve las recomendaciones PUBLIC."""
    return session.exec(
        select(BookRecommendation).where(BookRecommendation.visibility == "PUBLIC")
    ).all()

def obtener_recomendacion(rec_id: int, viewer_id: int, session: Session):
    """
    Devuelve una recomendación según su visibilidad:
    - PUBLIC: cualquiera puede verla
    - PRIVATE: solo el autor
    - FRIENDS: solo amigos aceptados
    """
    rec = session.get(BookRecommendation, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")

    if rec.visibility == "PUBLIC":
        return rec

    if rec.visibility == "PRIVATE":
        if rec.user_id != viewer_id:
            raise HTTPException(status_code=403, detail="No tienes acceso a esta recomendación")
        return rec

    if rec.visibility == "FRIENDS":
        if rec.user_id == viewer_id:
            return rec
        # Verifica si son amigos aceptados
        amistad = session.exec(
            select(Friendship).where(
                Friendship.status == "ACCEPTED",
                ((Friendship.requester_id == viewer_id) & (Friendship.receiver_id == rec.user_id)) |
                ((Friendship.requester_id == rec.user_id) & (Friendship.receiver_id == viewer_id))
            )
        ).first()
        if not amistad:
            raise HTTPException(status_code=403, detail="Solo amigos pueden ver esta recomendación")
        return rec

def crear_recomendacion(rec: BookRecommendation, session: Session):
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec

def eliminar_recomendacion(rec_id: int, session: Session):
    rec = session.get(BookRecommendation, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    session.delete(rec)
    session.commit()
    return {"mensaje": "Recomendación eliminada"}


# ─────────────────────────────────────────────────────────────────────────────
# SERVICIOS DE LISTA DE LECTURA
# ─────────────────────────────────────────────────────────────────────────────

def obtener_lista(user_id: int, session: Session):
    return session.exec(
        select(ReadingListItem).where(ReadingListItem.user_id == user_id)
    ).all()

def agregar_a_lista(item: ReadingListItem, session: Session):
    # Evita duplicados del mismo libro en la lista del mismo usuario
    existente = session.exec(
        select(ReadingListItem).where(
            ReadingListItem.user_id == item.user_id,
            ReadingListItem.book_id == item.book_id
        )
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="El libro ya está en tu lista")
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def eliminar_de_lista(item_id: int, session: Session):
    item = session.get(ReadingListItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    session.delete(item)
    session.commit()
    return {"mensaje": "Libro eliminado de la lista"}


# ─────────────────────────────────────────────────────────────────────────────
# SERVICIOS DE COMENTARIOS
# ─────────────────────────────────────────────────────────────────────────────

def obtener_comentarios(rec_id: int, session: Session):
    return session.exec(
        select(Comment).where(Comment.recommendation_id == rec_id)
    ).all()

def crear_comentario(comentario: Comment, session: Session):
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario

def eliminar_comentario(comment_id: int, session: Session):
    comentario = session.get(Comment, comment_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    session.delete(comentario)
    session.commit()
    return {"mensaje": "Comentario eliminado"}


# ─────────────────────────────────────────────────────────────────────────────
# SERVICIOS DE ETIQUETAS
# ─────────────────────────────────────────────────────────────────────────────

def obtener_tags(session: Session):
    return session.exec(select(Tag)).all()

def crear_tag(tag: Tag, session: Session):
    existente = session.exec(select(Tag).where(Tag.name == tag.name)).first()
    if existente:
        raise HTTPException(status_code=400, detail="La etiqueta ya existe")
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag

def agregar_tag_a_libro(book_id: int, tag_id: int, session: Session):
    # Evita duplicados
    existente = session.exec(
        select(BookTag).where(BookTag.book_id == book_id, BookTag.tag_id == tag_id)
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="El libro ya tiene esa etiqueta")
    book_tag = BookTag(book_id=book_id, tag_id=tag_id)
    session.add(book_tag)
    session.commit()
    return {"mensaje": "Etiqueta agregada al libro"}


# ─────────────────────────────────────────────────────────────────────────────
# SERVICIOS DE AMISTAD
# ─────────────────────────────────────────────────────────────────────────────

def enviar_solicitud(amistad: Friendship, session: Session):
    # No puede mandarse solicitud a sí mismo
    if amistad.requester_id == amistad.receiver_id:
        raise HTTPException(status_code=400, detail="No puedes enviarte una solicitud a ti mismo")
    # Verifica que no exista ya una solicitud
    existente = session.exec(
        select(Friendship).where(
            Friendship.requester_id == amistad.requester_id,
            Friendship.receiver_id == amistad.receiver_id
        )
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una solicitud entre estos usuarios")
    session.add(amistad)
    session.commit()
    session.refresh(amistad)
    return amistad

def responder_solicitud(friendship_id: int, nuevo_status: str, session: Session):
    opciones = ["ACCEPTED", "REJECTED", "BLOCKED"]
    if nuevo_status not in opciones:
        raise HTTPException(status_code=400, detail="Estado inválido")
    amistad = session.get(Friendship, friendship_id)
    if not amistad:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    amistad.status = nuevo_status
    amistad.updated_at = datetime.now().isoformat()
    session.commit()
    session.refresh(amistad)
    return amistad

def obtener_amistades(user_id: int, session: Session):
    return session.exec(
        select(Friendship).where(
            (Friendship.requester_id == user_id) | (Friendship.receiver_id == user_id)
        )
    ).all()
