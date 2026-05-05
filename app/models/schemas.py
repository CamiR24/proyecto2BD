from pydantic import BaseModel
from typing import Any, Optional, List, Union
from datetime import date


# ─── USER ───────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    userId: int
    name: str
    age: int
    country: str
    email: str
    createdAt: date
    isActive: bool
    preferredGenres: List[str]
    preferredDecades: List[str]
    preferredThemes: List[str]

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    country: Optional[str] = None
    email: Optional[str] = None
    isActive: Optional[bool] = None
    preferredGenres: Optional[List[str]] = None
    preferredDecades: Optional[List[str]] = None
    preferredThemes: Optional[List[str]] = None


# ─── MOVIE ──────────────────────────────────────────────────────────────────

class MovieCreate(BaseModel):
    movieId: int
    title: str
    year: int
    avgRating: float
    duration: int
    budget: float
    languages: List[str]
    releaseDate: date
    tagline: str

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    avgRating: Optional[float] = None
    duration: Optional[int] = None
    budget: Optional[float] = None
    languages: Optional[List[str]] = None
    releaseDate: Optional[date] = None
    tagline: Optional[str] = None


# ─── GENRE ──────────────────────────────────────────────────────────────────

class GenreCreate(BaseModel):
    genreId: int
    name: str
    description: str
    isMainstream: bool
    subgenres: List[str]

class GenreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    isMainstream: Optional[bool] = None
    subgenres: Optional[List[str]] = None


# ─── ACTOR ──────────────────────────────────────────────────────────────────

class ActorCreate(BaseModel):
    actorId: int
    name: str
    birthDate: date
    nationality: str
    isActive: bool
    oscars: int

class ActorUpdate(BaseModel):
    name: Optional[str] = None
    birthDate: Optional[date] = None
    nationality: Optional[str] = None
    isActive: Optional[bool] = None
    oscars: Optional[int] = None


# ─── DIRECTOR ───────────────────────────────────────────────────────────────

class DirectorCreate(BaseModel):
    directorId: int
    name: str
    gender: str
    birthDate: date
    nationality: str

class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    birthDate: Optional[date] = None
    nationality: Optional[str] = None


# ─── ACTOR+DIRECTOR (multi-label) ───────────────────────────────────────────

class ActorDirectorCreate(BaseModel):
    actorId: int
    directorId: int
    name: str
    gender: str
    birthDate: date
    nationality: str
    isActive: bool
    oscars: int