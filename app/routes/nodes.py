from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from app.database import get_db
from app.models.schemas import (
    UserCreate, UserUpdate,
    MovieCreate, MovieUpdate,
    GenreCreate, GenreUpdate,
    ActorCreate, ActorUpdate,
    DirectorCreate, DirectorUpdate,
    ActorDirectorCreate,
    PlatformCreate, PlatformUpdate,
    BulkPropertyUpdate
)
from typing import List
import csv
import io

router = APIRouter(prefix="/nodes", tags=["Nodes"])
db = get_db()


# ════════════════════════════════════════════════════════════════
# USER
# ════════════════════════════════════════════════════════════════

@router.post("/users", summary="Crear usuario (1 label)")
def create_user(user: UserCreate):
    query = """
    CREATE (u:User {
        userId: $userId, name: $name, age: $age, country: $country,
        email: $email, createdAt: date($createdAt), isActive: $isActive,
        preferredGenres: $preferredGenres, preferredDecades: $preferredDecades,
        preferredThemes: $preferredThemes
    }) RETURN u
    """
    with db.session() as s:
        result = s.run(query, **user.model_dump(mode="json"))
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="Error al crear usuario")
        return dict(record["u"])


@router.get("/users", summary="Obtener todos los usuarios")
def get_users(country: str = None, isActive: bool = None, limit: int = 50):
    filters = []
    params = {"limit": limit}
    if country:
        filters.append("u.country = $country")
        params["country"] = country
    if isActive is not None:
        filters.append("u.isActive = $isActive")
        params["isActive"] = isActive
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    query = f"MATCH (u:User) {where} RETURN u LIMIT $limit"
    with db.session() as s:
        result = s.run(query, **params)
        return [dict(r["u"]) for r in result]


@router.patch("/users/bulk/update", summary="Actualizar propiedades en múltiples usuarios")
def bulk_update_users(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"u.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User) WHERE u.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(u) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/users/bulk/delete", summary="Eliminar múltiples usuarios por país")
def bulk_delete_users(country: str):
    with db.session() as s:
        result = s.run(
            "MATCH (u:User {country: $country}) DETACH DELETE u RETURN count(u) as deleted",
            country=country
        )
        return {"deleted": result.single()["deleted"]}


@router.delete("/users/bulk/properties", summary="Eliminar propiedades de múltiples usuarios")
def bulk_delete_user_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"u.{p}" for p in properties])
    query = f"""
    MATCH (u:User)
    WHERE u.{filter_property} = $filter_value
       OR u.{filter_property} = toInteger($filter_value)
       OR u.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause}
    RETURN count(u) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}



@router.get("/users/{userId}", summary="Obtener un usuario por ID")
def get_user(userId: int):
    with db.session() as s:
        result = s.run("MATCH (u:User {userId: $userId}) RETURN u", userId=userId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return dict(record["u"])


@router.patch("/users/{userId}", summary="Actualizar propiedades de un usuario")
def update_user(userId: int, data: UserUpdate):
    updates = {k: v for k, v in data.model_dump(mode="json").items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No hay propiedades para actualizar")
    set_clause = ", ".join([f"u.{k} = ${k}" for k in updates])
    query = f"MATCH (u:User {{userId: $userId}}) SET {set_clause} RETURN u"
    with db.session() as s:
        result = s.run(query, userId=userId, **updates)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return dict(record["u"])




@router.delete("/users/{userId}", summary="Eliminar un usuario")
def delete_user(userId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (u:User {userId: $userId}) DETACH DELETE u RETURN count(u) as deleted",
            userId=userId
        )
        return {"deleted": result.single()["deleted"]}


    
    

@router.delete("/users/{userId}/properties", summary="Eliminar propiedades de 1 usuario")
def delete_user_properties(userId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"u.{p}" for p in properties])
    query = f"MATCH (u:User {{userId: $userId}}) REMOVE {remove_clause} RETURN u"
    with db.session() as s:
        result = s.run(query, userId=userId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return dict(record["u"])


# ════════════════════════════════════════════════════════════════
# MOVIE
# ════════════════════════════════════════════════════════════════

@router.post("/movies", summary="Crear película (1 label)")
def create_movie(movie: MovieCreate):
    query = """
    CREATE (m:Movie {
        movieId: $movieId, title: $title, year: $year, avgRating: $avgRating,
        duration: $duration, budget: $budget, languages: $languages,
        releaseDate: date($releaseDate), tagline: $tagline
    }) RETURN m
    """
    with db.session() as s:
        result = s.run(query, **movie.model_dump(mode="json"))
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="Error al crear película")
        return dict(record["m"])


@router.get("/movies", summary="Obtener todas las películas con filtros")
def get_movies(year: int = None, min_rating: float = None, limit: int = 50):
    filters = []
    params = {"limit": limit}
    if year:
        filters.append("m.year = $year")
        params["year"] = year
    if min_rating:
        filters.append("m.avgRating >= $min_rating")
        params["min_rating"] = min_rating
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    query = f"MATCH (m:Movie) {where} RETURN m LIMIT $limit"
    with db.session() as s:
        result = s.run(query, **params)
        return [dict(r["m"]) for r in result]


@router.patch("/movies/bulk/update", summary="Actualizar propiedades en múltiples películas")
def bulk_update_movies(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"m.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (m:Movie) WHERE m.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(m) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/movies/bulk/delete", summary="Eliminar múltiples películas por año")
def bulk_delete_movies(year: int):
    with db.session() as s:
        result = s.run(
            "MATCH (m:Movie {year: $year}) DETACH DELETE m RETURN count(m) as deleted",
            year=year
        )
        return {"deleted": result.single()["deleted"]}



@router.get("/movies/{movieId}", summary="Obtener una película por ID")
def get_movie(movieId: int):
    with db.session() as s:
        result = s.run("MATCH (m:Movie {movieId: $movieId}) RETURN m", movieId=movieId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return dict(record["m"])


@router.patch("/movies/{movieId}", summary="Actualizar propiedades de una película")
def update_movie(movieId: int, data: MovieUpdate):
    updates = {k: v for k, v in data.model_dump(mode="json").items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No hay propiedades para actualizar")
    set_clause = ", ".join([f"m.{k} = ${k}" for k in updates])
    query = f"MATCH (m:Movie {{movieId: $movieId}}) SET {set_clause} RETURN m"
    with db.session() as s:
        result = s.run(query, movieId=movieId, **updates)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return dict(record["m"])




@router.delete("/movies/{movieId}", summary="Eliminar una película")
def delete_movie(movieId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (m:Movie {movieId: $movieId}) DETACH DELETE m RETURN count(m) as deleted",
            movieId=movieId
        )
        return {"deleted": result.single()["deleted"]}




# ════════════════════════════════════════════════════════════════
# GENRE
# ════════════════════════════════════════════════════════════════

@router.post("/genres", summary="Crear género (1 label)")
def create_genre(genre: GenreCreate):
    query = """
    CREATE (g:Genre {
        genreId: $genreId, name: $name, description: $description,
        isMainstream: $isMainstream, subgenres: $subgenres
    }) RETURN g
    """
    with db.session() as s:
        result = s.run(query, **genre.model_dump())
        return dict(result.single()["g"])


@router.get("/genres", summary="Obtener todos los géneros")
def get_genres(isMainstream: bool = None):
    params = {}
    where = ""
    if isMainstream is not None:
        where = "WHERE g.isMainstream = $isMainstream"
        params["isMainstream"] = isMainstream
    with db.session() as s:
        result = s.run(f"MATCH (g:Genre) {where} RETURN g", **params)
        return [dict(r["g"]) for r in result]


@router.get("/genres/{genreId}", summary="Obtener un género por ID")
def get_genre(genreId: int):
    with db.session() as s:
        result = s.run("MATCH (g:Genre {genreId: $genreId}) RETURN g", genreId=genreId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Género no encontrado")
        return dict(record["g"])


@router.patch("/genres/{genreId}", summary="Actualizar un género")
def update_genre(genreId: int, data: GenreUpdate):
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    set_clause = ", ".join([f"g.{k} = ${k}" for k in updates])
    query = f"MATCH (g:Genre {{genreId: $genreId}}) SET {set_clause} RETURN g"
    with db.session() as s:
        result = s.run(query, genreId=genreId, **updates)
        return dict(result.single()["g"])


@router.delete("/genres/{genreId}", summary="Eliminar un género")
def delete_genre(genreId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (g:Genre {genreId: $genreId}) DETACH DELETE g RETURN count(g) as deleted",
            genreId=genreId
        )
        return {"deleted": result.single()["deleted"]}