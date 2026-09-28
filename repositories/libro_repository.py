from db.database import get_connection
from models.libro import Libro


class LibroRepository:
    def get_all(self, filtro=""):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id, isbn, titulo, autor, categoria, anio, stock_total, stock_disponible FROM libros"
        params = []
        if filtro:
            query += " WHERE titulo LIKE ? OR autor LIKE ? OR isbn LIKE ?"
            params = [f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"]
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [Libro(*row) for row in rows]

    def get_by_id(self, id_libro):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, isbn, titulo, autor, categoria, anio, stock_total, stock_disponible FROM libros WHERE id = ?", (id_libro,))
        row = cursor.fetchone()
        conn.close()
        return Libro(*row) if row else None

    def create(self, libro: Libro):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO libros (isbn, titulo, autor, categoria, anio, stock_total, stock_disponible)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (libro.isbn, libro.titulo, libro.autor, libro.categoria, libro.anio, libro.stock_total, libro.stock_disponible))
        conn.commit()
        conn.close()

    def update(self, libro: Libro):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE libros SET isbn=?, titulo=?, autor=?, categoria=?, anio=?, stock_total=?, stock_disponible=?
            WHERE id=?
        """, (libro.isbn, libro.titulo, libro.autor, libro.categoria, libro.anio, libro.stock_total, libro.stock_disponible, libro.id_libro))
        conn.commit()
        conn.close()

    def update_stock(self, id_libro, cambio):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE libros SET stock_disponible = stock_disponible + ? WHERE id = ?", (cambio, id_libro))
        conn.commit()
        conn.close()