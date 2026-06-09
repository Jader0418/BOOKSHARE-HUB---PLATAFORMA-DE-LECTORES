from sqlmodel import Session, select
from models import Book


def obtener_todos(session: Session):
    """Retorna todos los libros."""
    return session.exec(select(Book)).all()


def obtener_por_id(session: Session, book_id: int):
    """Retorna un libro por su id."""
    return session.get(Book, book_id)


def crear(session: Session, libro: Book):
    """Crea un nuevo libro."""
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro


def actualizar(session: Session, book_id: int, datos: Book):
    """Actualiza un libro existente."""
    libro = session.get(Book, book_id)
    if not libro:
        return None
    libro.title = datos.title
    libro.author = datos.author
    libro.isbn = datos.isbn
    libro.published_year = datos.published_year
    libro.cover_url = datos.cover_url
    session.commit()
    session.refresh(libro)
    return libro


def eliminar(session: Session, book_id: int):
    """Elimina un libro por su id."""
    libro = session.get(Book, book_id)
    if not libro:
        return None
    session.delete(libro)
    session.commit()
    return {"mensaje": "Libro eliminado"}
