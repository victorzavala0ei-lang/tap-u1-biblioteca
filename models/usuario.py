class UsuarioSistema:
    def __init__(self, id_usuario, username, password_hash, rol, activo=1):
        self.id_usuario = id_usuario
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.activo = activo