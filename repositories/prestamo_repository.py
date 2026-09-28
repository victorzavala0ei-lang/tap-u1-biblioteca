from db.database import get_connection


class PrestamoRepository:
    def create(self, lector_id, libro_id, fecha_prestamo, fecha_vencimiento):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prestamos (lector_id, libro_id, fecha_prestamo, fecha_vencimiento, estado)
            VALUES (?, ?, ?, ?, 'activo')
        """, (lector_id, libro_id, fecha_prestamo, fecha_vencimiento))
        conn.commit()
        conn.close()

    def registrar_devolucion(self, id_prestamo, fecha_devolucion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE prestamos SET fecha_devolucion = ?, estado = 'devuelto' WHERE id = ?
        """, (fecha_devolucion, id_prestamo))
        conn.commit()
        conn.close()

    def get_prestamos_con_join(self, filtro_estado="todos"):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT p.id, l.folio, l.nombre, b.isbn, b.titulo, p.fecha_prestamo, p.fecha_vencimiento, p.fecha_devolucion, p.estado, p.libro_id
            FROM prestamos p
            JOIN lectores l ON p.lector_id = l.id
            JOIN libros b ON p.libro_id = b.id
        """
        params = []
        if filtro_estado != "todos":
            query += " WHERE p.estado = ?"
            params.append(filtro_estado)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_prestamos_atrasados(self, fecha_hoy):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT p.id, l.folio, l.nombre, b.titulo, p.fecha_prestamo, p.fecha_vencimiento
            FROM prestamos p
            JOIN lectores l ON p.lector_id = l.id
            JOIN libros b ON p.libro_id = b.id
            WHERE p.estado = 'activo' AND p.fecha_vencimiento < ?
        """
        cursor.execute(query, (fecha_hoy,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def existe_prestamo_activo(self, lector_id, libro_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM prestamos
            WHERE lector_id = ? AND libro_id = ? AND estado = 'activo'
        """, (lector_id, libro_id))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def lector_tiene_prestamos_activos(self, lector_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE lector_id = ? AND estado = 'activo'", (lector_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0