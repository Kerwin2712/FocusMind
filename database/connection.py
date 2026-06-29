import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.models import Base

# Archivo de base de datos SQLite local por defecto
DEFAULT_LOCAL_DB = "sqlite:///focusmind.db"


def load_env():
    """Carga variables de entorno de manera manual desde el archivo .env si existe.
    
    Evita dependencias de librerías externas adicionales.
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        # Limpiar comillas si existieran en el valor
                        val = value.strip().strip("'").strip('"')
                        os.environ[key.strip()] = val
        except Exception as e:
            print(f"[Warning] No se pudo leer el archivo .env de forma manual: {e}")


# Cargar variables del .env
load_env()

# Obtener URL de base de datos de Postgres, fallback a SQLite local
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    print("[Database] URL de PostgreSQL detectada en el entorno.")
    db_uri = DATABASE_URL
else:
    print(f"[Database] Usando base de datos SQLite local por defecto ({DEFAULT_LOCAL_DB}).")
    db_uri = DEFAULT_LOCAL_DB

# Configuración del motor de base de datos con manejo de errores robusto
try:
    # SQLalchemy realiza parametrización de consultas de forma nativa para prevenir SQLi
    engine = create_engine(db_uri, echo=False, pool_pre_ping=True)
except Exception as e:
    print(f"[ERROR] Error al instanciar el motor de SQLAlchemy con la URI proporcionada: {e}")
    print("[Database] Cayendo en SQLite local para evitar el cierre de la aplicación.")
    engine = create_engine(DEFAULT_LOCAL_DB, echo=False)

# Sesiones de base de datos thread-safe y scoped para integración móvil
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def init_db():
    """Inicializa la base de datos creando todas las tablas del esquema si no existen.
    
    Maneja excepciones de conexión o creación de tablas de forma segura.
    """
    try:
        # Crea las tablas registradas en models.py
        Base.metadata.create_all(engine)
        print("[Database] Base de datos e inicialización de tablas completada exitosamente.")
        return True
    except Exception as e:
        print(f"[ERROR] Error crítico durante la inicialización de la base de datos: {e}")
        # Si falla PostgreSQL (ej: credenciales inválidas u offline), intentamos inicializar SQLite local
        if db_uri != DEFAULT_LOCAL_DB:
            print("[Database] Reintentando inicializar esquema sobre SQLite local...")
            try:
                local_engine = create_engine(DEFAULT_LOCAL_DB)
                Base.metadata.create_all(local_engine)
                # Re-vincular la Session al motor local
                Session.configure(bind=local_engine)
                print("[Database] Inicialización exitosa sobre SQLite tras el fallback de PostgreSQL.")
                return True
            except Exception as local_err:
                print(f"[ERROR] Fallback a SQLite también falló: {local_err}")
                return False
        return False
