from repositories.libro_repository import LibroRepository
from models.libro import Libro
import sqlite3


class LibroService:
    def __init__(self):
        self.repo = LibroRepository()

    def listar(self, filtro=""):
        return self.repo.get_all(filtro)

    def guardar(self, id_libro, isbn, titulo, autor, categoria, anio, stock_total):
        if not all([isbn, titulo, autor, categoria, str(anio), str(stock_total)]):
            raise ValueError("Todos los campos obligatorios deben ser llenados.")
        try:
            anio = int(anio)
            stock_total = int(stock_total)
            if stock_total < 0:
                raise ValueError("El stock no puede ser negativo.")
        except ValueError:
            raise ValueError("Año y Stock deben ser números enteros válidos.")

        if id_libro:
            libro_actual = self.repo.get_by_id(id_libro)
            prestados = libro_actual.stock_total - libro_actual.stock_disponible
            nuevo_disponible = stock_total - prestados
            if nuevo_disponible < 0:
                raise ValueError(f"No se puede reducir el stock total a {stock_total} porque hay {prestados} prestados actualmente.")

            libro = Libro(id_libro, isbn, titulo, autor, categoria, anio, stock_total, nuevo_disponible)
            try:
                self.repo.update(libro)
            except sqlite3.IntegrityError:
                raise ValueError("El ISBN proporcionado ya está registrado con otro libro.")
        else:
            libro = Libro(None, isbn, titulo, autor, categoria, anio, stock_total, stock_total)
            try:
                self.repo.create(libro)
            except sqlite3.IntegrityError:
                raise ValueError("El ISBN proporcionado ya está registrado.")