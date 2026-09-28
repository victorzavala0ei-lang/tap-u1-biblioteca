from db.database import hash_password
from repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def login(self, username, password):
        user = self.repo.get_by_username(username)
        if not user:
            raise ValueError("Usuario o contraseña incorrectos.")
        if not user.activo:
            raise ValueError("El usuario se encuentra inactivo en el sistema.")
        if user.password_hash != hash_password(password):
            raise ValueError("Usuario o contraseña incorrectos.")
        return user