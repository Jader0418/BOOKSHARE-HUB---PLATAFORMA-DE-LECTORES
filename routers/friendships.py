from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from database import SessionDep
from models import Friendship
import services.friendships as service

router = APIRouter(prefix="/amistades", tags=["Amistades"])

ESTADOS_VALIDOS = ["PENDING", "ACCEPTED", "REJECTED", "BLOCKED"]


@router.get("/")
def listar_amistades(session: SessionDep):
    """Retorna todas las amistades."""
    return service.obtener_todas(session)


@router.get("/{friendship_id}")
def obtener_amistad(friendship_id: int, session: SessionDep):
    """Retorna una amistad por su id."""
    amistad = service.obtener_por_id(session, friendship_id)
    if not amistad:
        raise HTTPException(status_code=404, detail="Amistad no encontrada")
    return amistad


@router.post("/")
def crear_amistad(amistad: Friendship, session: SessionDep):
    """Crea una solicitud de amistad."""
    if amistad.requester_id == amistad.receiver_id:
        raise HTTPException(status_code=400, detail="No puedes enviarte solicitud a ti mismo")
    resultado = service.crear(session, amistad)
    if not resultado:
        raise HTTPException(status_code=409, detail="Ya existe una relación entre estos usuarios")
    return resultado


@router.put("/{friendship_id}")
def actualizar_estado(friendship_id: int, nuevo_estado: str, session: SessionDep):
    """Actualiza el estado de una amistad."""
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Usa: {ESTADOS_VALIDOS}")
    amistad = service.actualizar_estado(session, friendship_id, nuevo_estado)
    if not amistad:
        raise HTTPException(status_code=404, detail="Amistad no encontrada")
    return amistad


@router.delete("/{friendship_id}")
def eliminar_amistad(friendship_id: int, session: SessionDep):
    """Elimina una amistad por su id."""
    resultado = service.eliminar(session, friendship_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Amistad no encontrada")
    return resultado
