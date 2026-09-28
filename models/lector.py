class Lector:
    def __init__(self, id_lector, folio, nombre, correo, telefono, tipo, activo=1):
        self.id_lector = id_lector
        self.folio = folio
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.tipo = tipo
        self.activo = activo