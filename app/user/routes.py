"""Rutas CRUD para el recurso usuario."""

from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

users_db: Dict[int, Dict] = {}
next_id = 1  # pylint: disable=invalid-name


class UserCreate(BaseModel):
    """Esquema para la creacion de un usuario.

    :param name: Nombre del usuario.
    :param email: Email del usuario.
    """

    name: str
    email: str


class UserUpdate(BaseModel):
    """Esquema para la actualizacion parcial de un usuario.

    :param name: Nombre del usuario (opcional).
    :param email: Email del usuario (opcional).
    """

    name: Optional[str] = None
    email: Optional[str] = None


@router.get("/user")
def list_users() -> List[Dict]:
    """Lista todos los usuarios.

    :return: Lista de usuarios.
    """
    return list(users_db.values())


@router.post("/user", status_code=201)
def create_user(user: UserCreate) -> Dict:
    """Crea un nuevo usuario.

    :param user: Datos del usuario a crear.
    :return: Usuario creado con su ID asignado.
    """
    global next_id  # pylint: disable=global-statement
    user_data = {"id": next_id, "name": user.name, "email": user.email}
    users_db[next_id] = user_data
    next_id += 1
    return user_data


@router.get("/user/{user_id}")
def get_user(user_id: int) -> Dict:
    """Obtiene un usuario por su ID.

    :param user_id: ID del usuario.
    :return: Datos del usuario.
    :raises HTTPException: Si el usuario no existe (404).
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@router.put("/user/{user_id}")
def replace_user(user_id: int, user: UserCreate) -> Dict:
    """Reemplaza completamente un usuario.

    :param user_id: ID del usuario a reemplazar.
    :param user: Nuevos datos del usuario.
    :return: Usuario actualizado.
    :raises HTTPException: Si el usuario no existe (404).
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = {"id": user_id, "name": user.name, "email": user.email}
    users_db[user_id] = user_data
    return user_data


@router.patch("/user/{user_id}")
def update_user(user_id: int, user: UserUpdate) -> Dict:
    """Actualiza parcialmente un usuario.

    :param user_id: ID del usuario a actualizar.
    :param user: Campos a actualizar.
    :return: Usuario actualizado.
    :raises HTTPException: Si el usuario no existe (404).
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name is not None:
        users_db[user_id]["name"] = user.name
    if user.email is not None:
        users_db[user_id]["email"] = user.email
    return users_db[user_id]


@router.delete("/user/{user_id}", status_code=204)
def delete_user(user_id: int) -> None:
    """Elimina un usuario.

    :param user_id: ID del usuario a eliminar.
    :raises HTTPException: Si el usuario no existe (404).
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
