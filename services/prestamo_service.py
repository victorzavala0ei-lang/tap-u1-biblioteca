from repositories.prestamo_repository import PrestamoRepository
from repositories.libro_repository import LibroRepository
from repositories.lector_repository import LectorRepository
from datetime import datetime, timedelta
import csv


class PrestamoService:
    def __init__(self):
        self.prestamo_repo = PrestamoRepository()
        self.libro_repo = LibroRepository()
        self.lector_repo = LectorRepository()

    def realizar_prestamo(self, lector_id, libro_id):
        lector = self.lector_repo.get_by_id(lector_id)
        if not lector or not lector.activo:
            raise ValueError("No se puede prestar a un lector inactivo o inexistente.")

        libro = self.libro_repo.get_by_id(libro_id)
        if not libro or libro.stock_disponible <= 0:
            raise ValueError("No hay ejemplares disponibles para préstamo de este libro.")

        if self.prestamo_repo.existe_prestamo_activo(lector_id, libro_id):
            raise ValueError("El lector ya tiene un préstamo activo de este mismo libro.")

        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        fecha_venc = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        self.prestamo_repo.create(lector_id, libro_id, fecha_hoy, fecha_venc)
        self.libro_repo.update_stock(libro_id, -1)

    def devolver_prestamo(self, id_prestamo, libro_id):
        fecha_devolucion = datetime.now().strftime("%Y-%m-%d")
        self.prestamo_repo.registrar_devolucion(id_prestamo, fecha_devolucion)
        self.libro_repo.update_stock(libro_id, 1)

    def listar_prestamos(self, filtro="todos"):
        return self.prestamo_repo.get_prestamos_con_join(filtro)

    def obtener_reporte_atrasados(self):
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return self.prestamo_repo.get_prestamos_atrasados(fecha_hoy)

    def exportar_atrasados_csv(self, ruta_archivo):
        atrasados = self.obtener_reporte_atrasados()
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID Prestamo", "Folio Lector", "Nombre Lector", "Titulo Libro", "Fecha Prestamo", "Fecha Vencimiento"])
            for row in atrasados:
                writer.writerow(row)