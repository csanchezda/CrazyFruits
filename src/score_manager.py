"""
Gestión simple de puntajes usando un archivo JSON local.

Funciones:
- cargar_puntajes: lee y devuelve la lista de puntajes (o una lista vacía)
- guardar_puntaje: añade un nuevo puntaje con timestamp
- obtener_mejores: devuelve los N mejores puntajes ordenados
"""

import json
import os
from datetime import datetime

SCORES_FILE = "scores.json"

def cargar_puntajes():
    """Carga los puntajes desde el archivo JSON (si existe) y los devuelve.

    Si el archivo no existe o está corrupto devuelve una lista vacía.
    """
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_puntaje(score, nombre):
    """Guarda un nuevo puntaje en el archivo con la fecha actual.

    El nombre se normaliza (espacios) y se adjunta el timestamp.
    """
    puntajes = cargar_puntajes()
    nuevo = {
        "nombre": nombre.strip() if nombre else "Player",
        "score": score,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    puntajes.append(nuevo)
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(puntajes, f, indent=4, ensure_ascii=False)

def obtener_mejores(n=5):
    """Devuelve los N mejores puntajes (ordenados de mayor a menor)."""
    puntajes = cargar_puntajes()
    return sorted(puntajes, key=lambda x: x["score"], reverse=True)[:n]
