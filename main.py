from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database import SessionDep, create_db_and_tables
from models import Book, BookRecommendation
import services

app = FastAPI(title="BookShare Hub")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ─── VISTAS HTML ─────────────────────────────────────────────────────────────

@app.get("/")
def inicio(request: Request, session: SessionDep):
    recomendaciones = services.obtener_recomendaciones_publicas(session)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"recomendaciones": recomendaciones}
    )

@app.get("/libros")
def vista_libros(request: Request, session: SessionDep):
    libros = services.obtener_libros(session)
    return templates.TemplateResponse(
        request=request,
        name="libros.html",
        context={"libros": libros}
    )

@app.get("/recomendaciones")
def vista_recomendaciones(request: Request, session: SessionDep):
    recomendaciones = services.obtener_recomendaciones_publicas(session)
    return templates.TemplateResponse(
        request=request,
        name="recomendaciones.html",
        context={"recomendaciones": recomendaciones}
    )


# ─── FORMULARIOS HTML ────────────────────────────────────────────────────────

@app.post("/libros/crear")
def crear_libro_form(
    request: Request,
    session: SessionDep,
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    published_year: int = Form(...),
    cover_url: str = Form("")
):
    try:
        libro = Book(
            title=title,
            author=author,
            isbn=isbn,
            published_year=published_year,
            cover_url=cover_url if cover_url else None
        )
        services.crear_libro(libro, session)
        return RedirectResponse(url="/libros", status_code=303)
    except Exception as e:
        libros = services.obtener_libros(session)
        return templates.TemplateResponse(
            request=request,
            name="libros.html",
            context={"libros": libros, "error": str(e)}
        )

@app.post("/libros/eliminar/{book_id}")
def eliminar_libro_form(book_id: int, session: SessionDep):
    services.eliminar_libro(book_id, session)
    return RedirectResponse(url="/libros", status_code=303)

@app.post("/recomendaciones/crear")
def crear_recomendacion_form(
    request: Request,
    session: SessionDep,
    user_id: int = Form(...),
    book_id: int = Form(...),
    short_review: str = Form(...),
    rating: int = Form(...),
    status: str = Form(...),
    visibility: str = Form(...)
):
    try:
        rec = BookRecommendation(
            user_id=user_id,
            book_id=book_id,
            short_review=short_review,
            rating=rating,
            status=status,
            visibility=visibility
        )
        services.crear_recomendacion(rec, session)
        return RedirectResponse(url="/recomendaciones", status_code=303)
    except Exception as e:
        recomendaciones = services.obtener_recomendaciones_publicas(session)
        return templates.TemplateResponse(
            request=request,
            name="recomendaciones.html",
            context={"recomendaciones": recomendaciones, "error": str(e)}
        )

@app.post("/recomendaciones/eliminar/{rec_id}")
def eliminar_recomendacion_form(rec_id: int, session: SessionDep):
    services.eliminar_recomendacion(rec_id, session)
    return RedirectResponse(url="/recomendaciones", status_code=303)


# ─── API ─────────────────────────────────────────────────────────────────────

@app.get("/api/usuarios/")
def listar_usuarios(session: SessionDep):
    return services.obtener_usuarios(session)

@app.get("/api/usuarios/{user_id}/")
def obtener_usuario(user_id: int, session: SessionDep):
    return services.obtener_usuario(user_id, session)

@app.post("/api/usuarios/")
def crear_usuario(usuario, session: SessionDep):
    return services.crear_usuario(usuario, session)

@app.put("/api/usuarios/{user_id}/")
def actualizar_usuario(user_id: int, datos, session: SessionDep):
    return services.actualizar_usuario(user_id, datos, session)

@app.delete("/api/usuarios/{user_id}/")
def eliminar_usuario(user_id: int, session: SessionDep):
    return services.eliminar_usuario(user_id, session)

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

@app.get("/api/lista/{user_id}/")
def obtener_lista(user_id: int, session: SessionDep):
    return services.obtener_lista(user_id, session)

@app.get("/api/comentarios/{rec_id}/")
def obtener_comentarios(rec_id: int, session: SessionDep):
    return services.obtener_comentarios(rec_id, session)

@app.get("/api/tags/")
def listar_tags(session: SessionDep):
    return services.obtener_tags(session)

@app.get("/api/amistades/{user_id}/")
def obtener_amistades(user_id: int, session: SessionDep):
    return services.obtener_amistades(user_id, session)
