from repositories.lector_repository import LectorRepository
from repositories.prestamo_repository import PrestamoRepository
from models.lector import Lector
import sqlite3


class LectorService:
    def __init__(self):
        self.repo = LectorRepository()
        self.prestamo_repo = PrestamoRepository()

    def listar(self, filtro=""):
        return self.repo.get_all(filtro)

    def guardar(self, id_lector, folio, nombre, correo, telefono, tipo):
        if not all([folio, nombre, correo, telefono, tipo]):
            raise ValueError("Todos los campos son obligatorios.")

        lector = Lector(id_lector, folio, nombre, correo, telefono, tipo)
        try:
            if id_lector:
                self.repo.update(lector)
            else:
                self.repo.create(lector)
        except sqlite3.IntegrityError:
            raise ValueError("El Folio o Correo ya está registrado para otro lector.")

    def cambiar_estado(self, id_lector, nuevo_estado):
        if nuevo_estado == 0:
            if self.prestamo_repo.lector_tiene_prestamos_activos(id_lector):
                raise ValueError("No se puede desactivar al lector porque tiene préstamos activos pendientes.")
        self.repo.toggle_activo(id_lector, nuevo_estado)