from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from database import engine, SessionDep, create_db_and_tables
from models import (
    User, Book, BookRecommendation,
    ReadingListItem, Comment, Tag, BookTag, Friendship
)
import services

app = FastAPI(title="BookShare Hub")

# ─── PLANTILLAS Y ARCHIVOS ESTÁTICOS ─────────────────────────────────────────
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ─── STARTUP ─────────────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ─── VISTAS HTML ─────────────────────────────────────────────────────────────

@app.get("/")
def inicio(request: Request, session: SessionDep):
    libros = services.obtener_libros(session)
    recomendaciones = services.obtener_recomendaciones_publicas(session)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "libros": libros,
        "recomendaciones": recomendaciones
    })

@app.get("/libros")
def vista_libros(request: Request, session: SessionDep):
    libros = services.obtener_libros(session)
    return templates.TemplateResponse("libros.html", {
        "request": request,
        "libros": libros
    })

@app.get("/recomendaciones")
def vista_recomendaciones(request: Request, session: SessionDep):
    recomendaciones = services.obtener_recomendaciones_publicas(session)
    return templates.TemplateResponse("recomendaciones.html", {
        "request": request,
        "recomendaciones": recomendaciones
    })


# ─── API USUARIOS ─────────────────────────────────────────────────────────────

@app.get("/api/usuarios/")
def listar_usuarios(session: SessionDep):
    return services.obtener_usuarios(session)

@app.get("/api/usuarios/{user_id}/")
def obtener_usuario(user_id: int, session: SessionDep):
    return services.obtener_usuario(user_id, session)

@app.post("/api/usuarios/")
def crear_usuario(usuario: User, session: SessionDep):
    return services.crear_usuario(usuario, session)

@app.put("/api/usuarios/{user_id}/")
def actualizar_usuario(user_id: int, datos: User, session: SessionDep):
    return services.actualizar_usuario(user_id, datos, session)

@app.delete("/api/usuarios/{user_id}/")
def eliminar_usuario(user_id: int, session: SessionDep):
    return services.eliminar_usuario(user_id, session)


# ─── API LIBROS ───────────────────────────────────────────────────────────────

@app.get("/api/libros/")
def listar_libros(session: SessionDep):
    return services.obtener_libros(session)

@app.get("/api/libros/{book_id}/")
def obtener_libro(book_id: int, session: SessionDep):
    return services.obtener_libro(book_id, session)

@app.post("/api/libros/")
def crear_libro(libro: Book, session: SessionDep):
    return services.crear_libro(libro, session)

@app.delete("/api/libros/{book_id}/")
def eliminar_libro(book_id: int, session: SessionDep):
    return services.eliminar_libro(book_id, session)


# ─── API RECOMENDACIONES ──────────────────────────────────────────────────────

@app.get("/api/recomendaciones/")
def listar_recomendaciones(session: SessionDep):
    return services.obtener_recomendaciones_publicas(session)

@app.get("/api/recomendaciones/{rec_id}/")
def obtener_recomendacion(rec_id: int, viewer_id: int, session: SessionDep):
    return services.obtener_recomendacion(rec_id, viewer_id, session)

@app.post("/api/recomendaciones/")
def crear_recomendacion(rec: BookRecommendation, session: SessionDep):
    return services.crear_recomendacion(rec, session)

@app.delete("/api/recomendaciones/{rec_id}/")
def eliminar_recomendacion(rec_id: int, session: SessionDep):
    return services.eliminar_recomendacion(rec_id, session)


# ─── API LISTA DE LECTURA ─────────────────────────────────────────────────────

@app.get("/api/lista/{user_id}/")
def obtener_lista(user_id: int, session: SessionDep):
    return services.obtener_lista(user_id, session)

@app.post("/api/lista/")
def agregar_a_lista(item: ReadingListItem, session: SessionDep):
    return services.agregar_a_lista(item, session)

@app.delete("/api/lista/{item_id}/")
def eliminar_de_lista(item_id: int, session: SessionDep):
    return services.eliminar_de_lista(item_id, session)


# ─── API COMENTARIOS ──────────────────────────────────────────────────────────

@app.get("/api/comentarios/{rec_id}/")
def obtener_comentarios(rec_id: int, session: SessionDep):
    return services.obtener_comentarios(rec_id, session)

@app.post("/api/comentarios/")
def crear_comentario(comentario: Comment, session: SessionDep):
    return services.crear_comentario(comentario, session)

@app.delete("/api/comentarios/{comment_id}/")
def eliminar_comentario(comment_id: int, session: SessionDep):
    return services.eliminar_comentario(comment_id, session)


# ─── API ETIQUETAS ────────────────────────────────────────────────────────────

@app.get("/api/tags/")
def listar_tags(session: SessionDep):
    return services.obtener_tags(session)

@app.post("/api/tags/")
def crear_tag(tag: Tag, session: SessionDep):
    return services.crear_tag(tag, session)

@app.post("/api/libros/{book_id}/tags/{tag_id}/")
def agregar_tag(book_id: int, tag_id: int, session: SessionDep):
    return services.agregar_tag_a_libro(book_id, tag_id, session)


# ─── API AMISTADES ────────────────────────────────────────────────────────────

@app.get("/api/amistades/{user_id}/")
def obtener_amistades(user_id: int, session: SessionDep):
    return services.obtener_amistades(user_id, session)

@app.post("/api/amistades/")
def enviar_solicitud(amistad: Friendship, session: SessionDep):
    return services.enviar_solicitud(amistad, session)

@app.put("/api/amistades/{friendship_id}/")
def responder_solicitud(friendship_id: int, nuevo_status: str, session: SessionDep):
    return services.responder_solicitud(friendship_id, nuevo_status, session)
