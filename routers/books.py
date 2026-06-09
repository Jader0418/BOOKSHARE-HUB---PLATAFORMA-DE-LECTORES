from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from database import SessionDep
from models import Book
import services.books as service

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.get("/")
def listar_libros(session: SessionDep):
    """Retorna todos los libros."""
    return service.obtener_todos(session)


@router.get("/{book_id}")
def obtener_libro(book_id: int, session: SessionDep):
    """Retorna un libro por su id."""
    libro = service.obtener_por_id(session, book_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.post("/")
def crear_libro(libro: Book, session: SessionDep):
    """Crea un nuevo libro."""
    return service.crear(session, libro)


@router.put("/{book_id}")
def actualizar_libro(book_id: int, datos: Book, session: SessionDep):
    """Actualiza un libro existente."""
    libro = service.actualizar(session, book_id, datos)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.delete("/{book_id}")
def eliminar_libro(book_id: int, session: SessionDep):
    """Elimina un libro por su id."""
    resultado = service.eliminar(session, book_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return resultado
