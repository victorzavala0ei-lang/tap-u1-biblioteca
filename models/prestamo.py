class Prestamo:
    def __init__(self, id_prestamo, lector_id, libro_id, fecha_prestamo, fecha_vencimiento, fecha_devolucion=None, estado="activo"):
        self.id_prestamo = id_prestamo
        self.lector_id = lector_id
        self.libro_id = libro_id
        self.fecha_prestamo = fecha_prestamo
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado