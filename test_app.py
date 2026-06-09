import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from main import app
from database import get_session

# ─── CONFIGURACIÓN DE BASE DE DATOS PARA TESTS ───────────────────────────────
# Usamos una BD en memoria para no afectar la BD real
engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

def get_session_test():
    with Session(engine_test) as session:
        yield session

# Reemplazamos la sesión real por la de pruebas
app.dependency_overrides[get_session] = get_session_test

# Creamos las tablas en la BD de pruebas
SQLModel.metadata.create_all(engine_test)

client = TestClient(app)


# ─── TESTS DE USUARIOS ────────────────────────────────────────────────────────

def test_crear_usuario():
    """Prueba que se pueda crear un usuario correctamente."""
    respuesta = client.post("/api/usuarios/", json={
        "username": "jader123",
        "email": "jader@gmail.com",
        "hashed_password": "clave123",
        "full_name": "Jader Perez"
    })
    assert respuesta.status_code == 200
    assert respuesta.json()["username"] == "jader123"

def test_listar_usuarios():
    """Prueba que se puedan listar los usuarios."""
    respuesta = client.get("/api/usuarios/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)

def test_obtener_usuario_no_existe():
    """Prueba que devuelva 404 si el usuario no existe."""
    respuesta = client.get("/api/usuarios/9999/")
    assert respuesta.status_code == 404


# ─── TESTS DE LIBROS ──────────────────────────────────────────────────────────

def test_crear_libro():
    """Prueba que se pueda crear un libro correctamente."""
    respuesta = client.post("/api/libros/", json={
        "title": "Cien años de soledad",
        "author": "Gabriel Garcia Marquez",
        "isbn": "9780060883287",
        "published_year": 1967
    })
    assert respuesta.status_code == 200
    assert respuesta.json()["title"] == "Cien años de soledad"

def test_libro_isbn_duplicado():
    """Prueba que no se pueda crear dos libros con el mismo ISBN."""
    client.post("/api/libros/", json={
        "title": "Libro Test",
        "author": "Autor Test",
        "isbn": "1234567890",
        "published_year": 2000
    })
    respuesta = client.post("/api/libros/", json={
        "title": "Otro Libro",
        "author": "Otro Autor",
        "isbn": "1234567890",
        "published_year": 2001
    })
    assert respuesta.status_code == 400


# ─── TESTS DE RECOMENDACIONES ─────────────────────────────────────────────────

def test_recomendacion_rating_invalido():
    """Prueba que no acepte rating fuera del rango 1-5."""
    respuesta = client.post("/api/recomendaciones/", json={
        "user_id": 1,
        "book_id": 1,
        "rating": 10,
        "short_review": "Muy buen libro",
        "visibility": "PUBLIC",
        "status": "read"
    })
    assert respuesta.status_code == 422

def test_recomendacion_visibility_invalida():
    """Prueba que no acepte visibilidad inválida."""
    respuesta = client.post("/api/recomendaciones/", json={
        "user_id": 1,
        "book_id": 1,
        "rating": 4,
        "short_review": "Buen libro",
        "visibility": "INVALIDA",
        "status": "read"
    })
    assert respuesta.status_code == 422


# ─── TESTS DE LISTA DE LECTURA ────────────────────────────────────────────────

def test_no_duplicados_en_lista():
    """Prueba que no se pueda agregar el mismo libro dos veces a la lista."""
    client.post("/api/lista/", json={
        "user_id": 1,
        "book_id": 1,
        "list_type": "want_to_read"
    })
    respuesta = client.post("/api/lista/", json={
        "user_id": 1,
        "book_id": 1,
        "list_type": "want_to_read"
    })
    assert respuesta.status_code == 400


# ─── TESTS DE AMISTAD ─────────────────────────────────────────────────────────

def test_solicitud_a_si_mismo():
    """Prueba que no se pueda enviar solicitud a uno mismo."""
    respuesta = client.post("/api/amistades/", json={
        "requester_id": 1,
        "receiver_id": 1,
        "status": "PENDING"
    })
    assert respuesta.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
