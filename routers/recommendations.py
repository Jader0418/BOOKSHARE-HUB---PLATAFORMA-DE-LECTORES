from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from database import SessionDep
from models import BookRecommendation
import services.recommendations as service

router = APIRouter(prefix="/recomendaciones", tags=["Recomendaciones"])

ESTADOS_VALIDOS = ["read", "reading", "want_to_read"]
VISIBILIDAD_VALIDA = ["PUBLIC", "PRIVATE", "FRIENDS"]


@router.get("/")
def listar_recomendaciones(session: SessionDep):
    """Retorna todas las recomendaciones públicas."""
    return service.obtener_todas(session)


@router.get("/visibles/{viewer_id}")
def listar_visibles(viewer_id: int, session: SessionDep):
    """Retorna recomendaciones visibles para un usuario según visibilidad y amistad."""
    return service.obtener_visibles(session, viewer_id)


@router.get("/{rec_id}")
def obtener_recomendacion(rec_id: int, session: SessionDep):
    """Retorna una recomendación por su id."""
    rec = service.obtener_por_id(session, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return rec


@router.post("/")
def crear_recomendacion(recomendacion: BookRecommendation, session: SessionDep):
    """Crea una nueva recomendación."""
    if recomendacion.status not in ESTADOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Usa: {ESTADOS_VALIDOS}")
    if recomendacion.visibility not in VISIBILIDAD_VALIDA:
        raise HTTPException(status_code=400, detail=f"Visibilidad inválida. Usa: {VISIBILIDAD_VALIDA}")
    if recomendacion.rating and (recomendacion.rating < 1 or recomendacion.rating > 5):
        raise HTTPException(status_code=400, detail="El rating debe estar entre 1 y 5")
    return service.crear(session, recomendacion)


@router.put("/{rec_id}")
def actualizar_recomendacion(rec_id: int, datos: BookRecommendation, session: SessionDep):
    """Actualiza una recomendación existente."""
    rec = service.actualizar(session, rec_id, datos)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return rec


@router.delete("/{rec_id}")
def eliminar_recomendacion(rec_id: int, session: SessionDep):
    """Elimina una recomendación por su id."""
    resultado = service.eliminar(session, rec_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return resultado
