from db.database import init_db
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main():
    init_db()

    def abrir_menu_principal(usuario):
        def al_cerrar_sesion():
            main()

        app = MainWindow(usuario, on_logout=al_cerrar_sesion)
        app.mainloop()

    login = LoginWindow(on_login_success=abrir_menu_principal)
    login.mainloop()


if __name__ == "__main__":
    main()