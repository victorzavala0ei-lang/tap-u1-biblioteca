from db.database import get_connection
from models.lector import Lector


class LectorRepository:
    def get_all(self, filtro=""):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id, folio, nombre, correo, telefono, tipo, activo FROM lectores"
        params = []
        if filtro:
            query += " WHERE nombre LIKE ? OR folio LIKE ? OR correo LIKE ?"
            params = [f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"]
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [Lector(*row) for row in rows]

    def get_by_id(self, id_lector):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, folio, nombre, correo, telefono, tipo, activo FROM lectores WHERE id = ?", (id_lector,))
        row = cursor.fetchone()
        conn.close()
        return Lector(*row) if row else None

    def create(self, lector: Lector):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO lectores (folio, nombre, correo, telefono, tipo, activo)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (lector.folio, lector.nombre, lector.correo, lector.telefono, lector.tipo))
        conn.commit()
        conn.close()

    def update(self, lector: Lector):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE lectores SET folio=?, nombre=?, correo=?, telefono=?, tipo=? WHERE id=?
        """, (lector.folio, lector.nombre, lector.correo, lector.telefono, lector.tipo, lector.id_lector))
        conn.commit()
        conn.close()

    def toggle_activo(self, id_lector, estado):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE lectores SET activo = ? WHERE id = ?", (estado, id_lector))
        conn.commit()
        conn.close()