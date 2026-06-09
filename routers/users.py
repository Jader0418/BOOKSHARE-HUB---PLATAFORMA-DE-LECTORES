from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from database import SessionDep
from models import User
import services.users as service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/")
def listar_usuarios(session: SessionDep):
    """Retorna todos los usuarios."""
    return service.obtener_todos(session)


@router.get("/{user_id}")
def obtener_usuario(user_id: int, session: SessionDep):
    """Retorna un usuario por su id."""
    usuario = service.obtener_por_id(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/")
def crear_usuario(usuario: User, session: SessionDep):
    """Crea un nuevo usuario."""
    return service.crear(session, usuario)


@router.put("/{user_id}")
def actualizar_usuario(user_id: int, datos: User, session: SessionDep):
    """Actualiza un usuario existente."""
    usuario = service.actualizar(session, user_id, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{user_id}")
def eliminar_usuario(user_id: int, session: SessionDep):
    """Elimina un usuario por su id."""
    resultado = service.eliminar(session, user_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return resultado
