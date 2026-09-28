from db.database import get_connection
from models.usuario import UsuarioSistema


class UsuarioRepository:
    def get_by_username(self, username: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, rol, activo FROM usuarios_sistema WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return UsuarioSistema(*row) if row else None