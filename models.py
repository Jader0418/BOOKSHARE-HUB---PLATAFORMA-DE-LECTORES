from typing import Optional
from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel


# ─── USUARIO ─────────────────────────────────────────────────────────────────

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str
    full_name: str = Field(..., min_length=3)
    is_active: bool = Field(default=True)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator("username", "full_name")
    @classmethod
    def validar_texto(cls, valor):
        if not valor.strip():
            raise ValueError("El campo no puede estar vacío")
        return valor.strip()


# ─── LIBRO ───────────────────────────────────────────────────────────────────

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=3)
    isbn: str = Field(..., min_length=10, max_length=13)
    published_year: int = Field(..., ge=1000, le=2100)
    cover_url: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


# ─── RECOMENDACIÓN ───────────────────────────────────────────────────────────

class BookRecommendation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")
    status: str = Field(default="want_to_read")
    rating: int = Field(..., ge=1, le=5)
    short_review: str = Field(..., min_length=5, max_length=300)
    visibility: str = Field(default="PUBLIC")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator("status")
    @classmethod
    def validar_status(cls, valor):
        opciones = ["read", "reading", "want_to_read"]
        if valor not in opciones:
            raise ValueError("Estado debe ser: read, reading o want_to_read")
        return valor

    @field_validator("visibility")
    @classmethod
    def validar_visibility(cls, valor):
        opciones = ["PUBLIC", "PRIVATE", "FRIENDS"]
        if valor not in opciones:
            raise ValueError("Visibilidad debe ser: PUBLIC, PRIVATE o FRIENDS")
        return valor


# ─── LISTA DE LECTURA ────────────────────────────────────────────────────────

class ReadingListItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")
    list_type: str = Field(default="want_to_read")
    notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


# ─── COMENTARIO ──────────────────────────────────────────────────────────────

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    recommendation_id: int = Field(foreign_key="bookrecommendation.id")
    content: str = Field(..., min_length=2, max_length=500)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


# ─── ETIQUETA ────────────────────────────────────────────────────────────────

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=2, max_length=50)


# ─── RELACIÓN LIBRO-ETIQUETA ─────────────────────────────────────────────────

class BookTag(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


# ─── AMISTAD ─────────────────────────────────────────────────────────────────

class Friendship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    requester_id: int = Field(foreign_key="user.id")
    receiver_id: int = Field(foreign_key="user.id")
    status: str = Field(default="PENDING")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator("status")
    @classmethod
    def validar_status(cls, valor):
        opciones = ["PENDING", "ACCEPTED", "REJECTED", "BLOCKED"]
        if valor not in opciones:
            raise ValueError("Estado debe ser: PENDING, ACCEPTED, REJECTED o BLOCKED")
        return valor
