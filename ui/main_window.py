import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.libro_service import LibroService
from services.lector_service import LectorService
from services.prestamo_service import PrestamoService


class MainWindow(tk.Tk):
    def __init__(self, usuario, on_logout):
        super().__init__()
        self.usuario = usuario
        self.on_logout = on_logout
        self.title(f"Biblioteca Digital | Usuario: {usuario.username} ({usuario.rol})")
        self.geometry("950x600")

        self.libro_service = LibroService()
        self.lector_service = LectorService()
        self.prestamo_service = PrestamoService()

        style = ttk.Style(self)
        style.theme_use('clam')

        self.crear_menu()

        header = ttk.Frame(self, padding=10, relief="groove")
        header.pack(fill="x")
        ttk.Label(header, text=f"Sesión activa: {usuario.username} | Rol: {usuario.rol.upper()}", font=("Arial", 10, "italic")).pack(side="left")
        ttk.Button(header, text="Cerrar Sesión", command=self.cerrar_sesion).pack(side="right")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_libros = ttk.Frame(self.notebook)
        self.tab_lectores = ttk.Frame(self.notebook)
        self.tab_prestamos = ttk.Frame(self.notebook)
        self.tab_reporte = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_libros, text=" Libros (Entidad A) ")
        self.notebook.add(self.tab_lectores, text=" Lectores (Entidad B) ")
        self.notebook.add(self.tab_prestamos, text=" Préstamos & Devoluciones ")
        self.notebook.add(self.tab_reporte, text=" Reporte Atrasados ")

        self.build_tab_libros()
        self.build_tab_lectores()
        self.build_tab_prestamos()
        self.build_tab_reporte()

    def crear_menu(self):
        menubar = tk.Menu(self)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        self.config(menu=menubar)

    def cerrar_sesion(self):
        self.destroy()
        self.on_logout()

    def build_tab_libros(self):
        frame_top = ttk.Frame(self.tab_libros, padding=5)
        frame_top.pack(fill="x")

        ttk.Label(frame_top, text="Buscar:").pack(side="left")
        self.txt_busca_libro = ttk.Entry(frame_top)
        self.txt_busca_libro.pack(side="left", padx=5)
        ttk.Button(frame_top, text="Filtrar", command=self.cargar_libros).pack(side="left")

        ttk.Button(frame_top, text="Nuevo Libro", command=self.form_libro).pack(side="right")
        ttk.Button(frame_top, text="Editar Seleccionado", command=self.editar_libro_sel).pack(side="right", padx=5)

        cols = ("id", "isbn", "titulo", "autor", "categoria", "anio", "stock_t", "stock_d")
        self.tree_libros = ttk.Treeview(self.tab_libros, columns=cols, show="headings")
        for col in cols:
            self.tree_libros.heading(col, text=col.upper())
            self.tree_libros.column(col, width=100)
        self.tree_libros.pack(fill="both", expand=True, pady=5)
        self.cargar_libros()

    def cargar_libros(self):
        for item in self.tree_libros.get_children():
            self.tree_libros.delete(item)
        filtro = self.txt_busca_libro.get().strip()
        for l in self.libro_service.listar(filtro):
            self.tree_libros.insert("", "end", values=(l.id_libro, l.isbn, l.titulo, l.autor, l.categoria, l.anio, l.stock_total, l.stock_disponible))

    def form_libro(self, libro=None):
        top = tk.Toplevel(self)
        top.title("Formulario Libro")
        top.geometry("300x350")

        fields = ["ISBN", "Título", "Autor", "Categoría", "Año", "Stock Total"]
        entries = {}
        for f in fields:
            ttk.Label(top, text=f+":").pack(anchor="w", padx=10, pady=2)
            e = ttk.Entry(top)
            e.pack(fill="x", padx=10)
            entries[f] = e

        if libro:
            entries["ISBN"].insert(0, libro.isbn)
            entries["Título"].insert(0, libro.titulo)
            entries["Autor"].insert(0, libro.autor)
            entries["Categoría"].insert(0, libro.categoria)
            entries["Año"].insert(0, str(libro.anio))
            entries["Stock Total"].insert(0, str(libro.stock_total))

        def guardar():
            try:
                id_l = libro.id_libro if libro else None
                self.libro_service.guardar(
                    id_l,
                    entries["ISBN"].get().strip(),
                    entries["Título"].get().strip(),
                    entries["Autor"].get().strip(),
                    entries["Categoría"].get().strip(),
                    entries["Año"].get().strip(),
                    entries["Stock Total"].get().strip()
                )
                messagebox.showinfo("Éxito", "Libro guardado exitosamente.")
                top.destroy()
                self.cargar_libros()
            except ValueError as ex:
                messagebox.showerror("Error de Validación", str(ex))

        ttk.Button(top, text="Guardar", command=guardar).pack(pady=15)

    def editar_libro_sel(self):
        sel = self.tree_libros.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un libro para editar.")
            return
        vals = self.tree_libros.item(sel[0], "values")
        libro = self.libro_service.repo.get_by_id(vals[0])
        self.form_libro(libro)

    def build_tab_lectores(self):
        frame_top = ttk.Frame(self.tab_lectores, padding=5)
        frame_top.pack(fill="x")

        ttk.Label(frame_top, text="Buscar:").pack(side="left")
        self.txt_busca_lector = ttk.Entry(frame_top)
        self.txt_busca_lector.pack(side="left", padx=5)
        ttk.Button(frame_top, text="Filtrar", command=self.cargar_lectores).pack(side="left")

        ttk.Button(frame_top, text="Nuevo Lector", command=self.form_lector).pack(side="right")
        ttk.Button(frame_top, text="Editar", command=self.editar_lector_sel).pack(side="right", padx=5)
        ttk.Button(frame_top, text="Activar/Desactivar", command=self.toggle_lector_sel).pack(side="right", padx=5)

        cols = ("id", "folio", "nombre", "correo", "telefono", "tipo", "activo")
        self.tree_lectores = ttk.Treeview(self.tab_lectores, columns=cols, show="headings")
        for col in cols:
            self.tree_lectores.heading(col, text=col.upper())
            self.tree_lectores.column(col, width=100)
        self.tree_lectores.pack(fill="both", expand=True, pady=5)
        self.cargar_lectores()

    def cargar_lectores(self):
        for item in self.tree_lectores.get_children():
            self.tree_lectores.delete(item)
        filtro = self.txt_busca_lector.get().strip()
        for l in self.lector_service.listar(filtro):
            st = "Activo" if l.activo else "Inactivo"
            self.tree_lectores.insert("", "end", values=(l.id_lector, l.folio, l.nombre, l.correo, l.telefono, l.tipo, st))

    def form_lector(self, lector=None):
        top = tk.Toplevel(self)
        top.title("Formulario Lector")
        top.geometry("300x320")

        fields = ["Folio", "Nombre", "Correo", "Teléfono", "Tipo (alumno/docente/externo)"]
        entries = {}
        for f in fields:
            ttk.Label(top, text=f+":").pack(anchor="w", padx=10, pady=2)
            e = ttk.Entry(top)
            e.pack(fill="x", padx=10)
            entries[f] = e

        if lector:
            entries["Folio"].insert(0, lector.folio)
            entries["Nombre"].insert(0, lector.nombre)
            entries["Correo"].insert(0, lector.correo)
            entries["Teléfono"].insert(0, lector.telefono)
            entries["Tipo (alumno/docente/externo)"].insert(0, lector.tipo)

        def guardar():
            try:
                id_lec = lector.id_lector if lector else None
                self.lector_service.guardar(
                    id_lec,
                    entries["Folio"].get().strip(),
                    entries["Nombre"].get().strip(),
                    entries["Correo"].get().strip(),
                    entries["Teléfono"].get().strip(),
                    entries["Tipo (alumno/docente/externo)"].get().strip()
                )
                messagebox.showinfo("Éxito", "Lector guardado correctamente.")
                top.destroy()
                self.cargar_lectores()
            except ValueError as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(top, text="Guardar", command=guardar).pack(pady=15)

    def editar_lector_sel(self):
        sel = self.tree_lectores.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un lector.")
            return
        vals = self.tree_lectores.item(sel[0], "values")
        lector = self.lector_service.repo.get_by_id(vals[0])
        self.form_lector(lector)

    def toggle_lector_sel(self):
        sel = self.tree_lectores.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un lector.")
            return
        vals = self.tree_lectores.item(sel[0], "values")
        id_lector = vals[0]
        estado_actual = 1 if vals[6] == "Activo" else 0
        nuevo_estado = 0 if estado_actual == 1 else 1

        if messagebox.askyesno("Confirmar Acción", f"¿Está seguro de que desea cambiar el estado del lector ID {id_lector}?"):
            try:
                self.lector_service.cambiar_estado(id_lector, nuevo_estado)
                messagebox.showinfo("Éxito", "Estado cambiado correctamente.")
                self.cargar_lectores()
            except ValueError as ex:
                messagebox.showerror("Acción Denegada", str(ex))

    def build_tab_prestamos(self):
        f_top = ttk.Frame(self.tab_prestamos, padding=5)
        f_top.pack(fill="x")

        ttk.Button(f_top, text="Registrar Nuevo Préstamo", command=self.form_prestamo).pack(side="left")
        ttk.Button(f_top, text="Registrar Devolución", command=self.devolver_sel).pack(side="left", padx=10)

        cols = ("ID", "Folio Lector", "Lector", "ISBN Libro", "Libro", "Fecha Prestamo", "Vencimiento", "Devolucion", "Estado")
        self.tree_prestamos = ttk.Treeview(self.tab_prestamos, columns=cols, show="headings")
        for c in cols:
            self.tree_prestamos.heading(c, text=c)
            self.tree_prestamos.column(c, width=100)
        self.tree_prestamos.pack(fill="both", expand=True, pady=5)
        self.cargar_prestamos()

    def cargar_prestamos(self):
        for item in self.tree_prestamos.get_children():
            self.tree_prestamos.delete(item)
        for row in self.prestamo_service.listar_prestamos():
            dev = row[7] if row[7] else "-"
            self.tree_prestamos.insert("", "end", iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], dev, row[8]))

    def form_prestamo(self):
        top = tk.Toplevel(self)
        top.title("Alta de Préstamo")
        top.geometry("380x200")

        ttk.Label(top, text="Seleccione Lector:").pack(anchor="w", padx=10, pady=2)
        lectores = self.lector_service.listar()
        combo_lector = ttk.Combobox(top, state="readonly", values=[f"{l.id_lector} - {l.nombre} ({l.folio})" for l in lectores if l.activo])
        combo_lector.pack(fill="x", padx=10)

        ttk.Label(top, text="Seleccione Libro:").pack(anchor="w", padx=10, pady=2)
        libros = self.libro_service.listar()
        combo_libro = ttk.Combobox(top, state="readonly", values=[f"{b.id_libro} - {b.titulo} (Disp: {b.stock_disponible})" for b in libros])
        combo_libro.pack(fill="x", padx=10)

        def realizar():
            if not combo_lector.get() or not combo_libro.get():
                messagebox.showerror("Error", "Debe seleccionar un lector y un libro.")
                return
            id_lec = int(combo_lector.get().split(" - ")[0])
            id_lib = int(combo_libro.get().split(" - ")[0])

            try:
                self.prestamo_service.realizar_prestamo(id_lec, id_lib)
                messagebox.showinfo("Éxito", "Préstamo registrado exitosamente (vigencia: 7 días).")
                top.destroy()
                self.cargar_prestamos()
                self.cargar_libros()
            except ValueError as ex:
                messagebox.showerror("Regla de Negocio Violada", str(ex))

        ttk.Button(top, text="Confirmar Préstamo", command=realizar).pack(pady=15)

    def devolver_sel(self):
        sel = self.tree_prestamos.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un préstamo activo de la lista.")
            return

        vals = self.tree_prestamos.item(sel[0], "values")
        id_prestamo = vals[0]
        estado = vals[8]

        if estado == "devuelto":
            messagebox.showinfo("Información", "Este préstamo ya ha sido devuelto previamente.")
            return

        if messagebox.askyesno("Confirmar Devolución", f"¿Desea registrar la devolución del préstamo ID {id_prestamo}?"):
            for row in self.prestamo_service.listar_prestamos():
                if row[0] == int(id_prestamo):
                    libro_id = row[9]
                    break
            self.prestamo_service.devolver_prestamo(id_prestamo, libro_id)
            messagebox.showinfo("Éxito", "Devolución registrada correctamente y stock reincorporado.")
            self.cargar_prestamos()
            self.cargar_libros()

    def build_tab_reporte(self):
        f_top = ttk.Frame(self.tab_reporte, padding=5)
        f_top.pack(fill="x")

        ttk.Button(f_top, text="Actualizar Reporte", command=self.cargar_reporte).pack(side="left")
        ttk.Button(f_top, text="Exportar a CSV", command=self.exportar_csv).pack(side="right")

        cols = ("ID Préstamo", "Folio Lector", "Nombre Lector", "Título Libro", "Fecha Préstamo", "Fecha Vencimiento")
        self.tree_reporte = ttk.Treeview(self.tab_reporte, columns=cols, show="headings")
        for c in cols:
            self.tree_reporte.heading(c, text=c)
            self.tree_reporte.column(c, width=120)
        self.tree_reporte.pack(fill="both", expand=True, pady=5)
        self.cargar_reporte()

    def cargar_reporte(self):
        for item in self.tree_reporte.get_children():
            self.tree_reporte.delete(item)
        atrasados = self.prestamo_service.obtener_reporte_atrasados()
        for row in atrasados:
            self.tree_reporte.insert("", "end", values=row)

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if ruta:
            try:
                self.prestamo_service.exportar_atrasados_csv(ruta)
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente a:\n{ruta}")
            except Exception as ex:
                messagebox.showerror("Error", f"Falló al exportar CSV: {str(ex)}")