import sqlite3
import hashlib

DB_NAME = "biblioteca.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios_sistema (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL,
        activo INTEGER NOT NULL DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isbn TEXT UNIQUE NOT NULL,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        categoria TEXT NOT NULL,
        anio INTEGER NOT NULL,
        stock_total INTEGER NOT NULL,
        stock_disponible INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lectores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folio TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        correo TEXT UNIQUE NOT NULL,
        telefono TEXT NOT NULL,
        tipo TEXT NOT NULL,
        activo INTEGER NOT NULL DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prestamos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lector_id INTEGER NOT NULL,
        libro_id INTEGER NOT NULL,
        fecha_prestamo TEXT NOT NULL,
        fecha_vencimiento TEXT NOT NULL,
        fecha_devolucion TEXT,
        estado TEXT NOT NULL DEFAULT 'activo',
        FOREIGN KEY (lector_id) REFERENCES lectores(id),
        FOREIGN KEY (libro_id) REFERENCES libros(id)
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM usuarios_sistema;")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios_sistema (username, password_hash, rol, activo) VALUES (?, ?, ?, 1)",
                       ("admin", hash_password("admin123"), "administrador"))
        cursor.execute("INSERT INTO usuarios_sistema (username, password_hash, rol, activo) VALUES (?, ?, ?, 1)",
                       ("operador", hash_password("operador123"), "operador"))

    cursor.execute("SELECT COUNT(*) FROM libros;")
    if cursor.fetchone()[0] == 0:
        libros_demo = [
            ("9780131103627", "El Lenguaje de Programacion C", "Brian Kernighan", "Sistemas", 1988, 5, 5),
            ("9780132350884", "Clean Code", "Robert C. Martin", "Software", 2008, 3, 2),
            ("9780201633610", "Design Patterns", "Erich Gamma", "Software", 1994, 4, 3),
            ("9780596007126", "Head First Design Patterns", "Eric Freeman", "Software", 2004, 2, 2),
            ("9780262033848", "Introduction to Algorithms", "Thomas H. Cormen", "Algoritmos", 2009, 2, 1),
            ("9781449355739", "Learning Python", "Mark Lutz", "Programacion", 2013, 3, 3),
            ("9780134685991", "Effective Java", "Joshua Bloch", "Programacion", 2017, 2, 2),
            ("9780596517748", "JavaScript: The Good Parts", "Douglas Crockford", "Web", 2008, 1, 0)
        ]
        cursor.executemany("""
            INSERT INTO libros (isbn, titulo, autor, categoria, anio, stock_total, stock_disponible)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, libros_demo)

    cursor.execute("SELECT COUNT(*) FROM lectores;")
    if cursor.fetchone()[0] == 0:
        lectores_demo = [
            ("LEC-001", "Carlos Gomez", "carlos@estudiante.edu", "8331112233", "alumno", 1),
            ("LEC-002", "Ana Martinez", "ana@docente.edu", "8332223344", "docente", 1),
            ("LEC-003", "Luis Hernandez", "luis@estudiante.edu", "8333334455", "alumno", 1),
            ("LEC-004", "Maria Rodriguez", "maria@externo.org", "8334445566", "externo", 1),
            ("LEC-005", "Pedro Infante", "pedro@inactivo.edu", "8335556677", "alumno", 0)
        ]
        cursor.executemany("""
            INSERT INTO lectores (folio, nombre, correo, telefono, tipo, activo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, lectores_demo)

    cursor.execute("SELECT COUNT(*) FROM prestamos;")
    if cursor.fetchone()[0] == 0:
        prestamos_demo = [
            (1, 2, "2026-09-25", "2026-10-02", None, "activo"),
            (2, 3, "2026-09-01", "2026-09-08", None, "activo"),
            (3, 5, "2026-08-10", "2026-08-17", "2026-08-15", "devuelto")
        ]
        cursor.executemany("""
            INSERT INTO prestamos (lector_id, libro_id, fecha_prestamo, fecha_vencimiento, fecha_devolucion, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, prestamos_demo)

    conn.commit()
    conn.close()