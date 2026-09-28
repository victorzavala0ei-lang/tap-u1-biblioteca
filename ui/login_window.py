import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService


class LoginWindow(tk.Tk):
    def __init__(self, on_login_success):
        super().__init__()
        self.title("Acceso al Sistema - Biblioteca Tkinter")
        self.geometry("380x280")
        self.resizable(False, False)
        self.auth_service = AuthService()
        self.on_login_success = on_login_success

        style = ttk.Style(self)
        style.theme_use('clam')

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Sistema de Biblioteca", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Label(container, text="Usuario:").pack(anchor="w")
        self.txt_user = ttk.Entry(container, width=30)
        self.txt_user.pack(pady=5)

        ttk.Label(container, text="Contraseña:").pack(anchor="w")
        self.txt_pass = ttk.Entry(container, show="*", width=30)
        self.txt_pass.pack(pady=5)

        btn_login = ttk.Button(container, text="Iniciar Sesión", command=self.ejecutar_login)
        btn_login.pack(pady=15)

    def ejecutar_login(self):
        username = self.txt_user.get().strip()
        password = self.txt_pass.get().strip()

        try:
            usuario = self.auth_service.login(username, password)
            self.destroy()
            self.on_login_success(usuario)
        except ValueError as err:
            messagebox.showerror("Error de Autenticación", str(err))