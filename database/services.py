import json
from sqlalchemy.orm import Session as SqlalchemySession
from database.connection import Session
from database.models import Usuario, Habito, EstadoEntorno, HistorialDopamina

# Hábitos Freemium por defecto
DEFAULT_HABITS = [
    {
        "nombre": "Tender la cama",
        "descripcion": "Hábito matutino predefinido",
    },
    {
        "nombre": "Leer páginas de un libro",
        "descripcion": "Mínimo 10 páginas diarias",
    },
    {
        "nombre": "Ordenar la ropa",
        "descripcion": "Mantener el cuarto limpio",
    },
]


def get_or_create_default_user() -> Usuario:
    """Obtiene el usuario por defecto (ID 1) o lo crea si no existe.
    
    Asegura una persistencia segura de inicio rápido.
    """
    session = Session()
    try:
        user = session.query(Usuario).filter(Usuario.id == 1).first()
        if not user:
            # Crear usuario inicial por defecto
            user = Usuario(
                id=1,
                email="default@focusmind.com",
                password_hash="pbkdf2:sha256:default_hash_value",  # Placeholder seguro
                tipo_plan="Free"
            )
            session.add(user)
            session.commit()
            
            # Crear estado de entorno inicial
            entorno = EstadoEntorno(
                user_id=1,
                habitacion_level=1,
                items_ordenados_json=json.dumps({
                    "cama": "messy",
                    "libros": "messy",
                    "ropa": "messy"
                })
            )
            session.add(entorno)
            session.commit()
            
            # Refrescar instancia
            session.refresh(user)
            print("[Database] Usuario por defecto y entorno inicial creados con éxito.")
        return user
    except Exception as e:
        session.rollback()
        print(f"[Database ERROR] Error al obtener/crear usuario por defecto: {e}")
        raise e
    finally:
        session.close()


def get_user_habits(user_id: int) -> list[Habito]:
    """Carga los hábitos del usuario.
    
    Si es la primera vez que ingresa, inicializa los 3 hábitos Freemium por defecto.
    """
    # Asegurar que el usuario exista
    get_or_create_default_user()
    
    session = Session()
    try:
        habitos = session.query(Habito).filter(Habito.user_id == user_id).all()
        if not habitos:
            # Inicializar hábitos Freemium
            print(f"[Database] Inicializando hábitos por defecto para usuario {user_id}...")
            habitos = []
            for h_def in DEFAULT_HABITS:
                nuevo_habito = Habito(
                    user_id=user_id,
                    nombre=h_def["nombre"],
                    descripcion=h_def["descripcion"],
                    estado_actual=False,
                    racha_actual=0
                )
                session.add(nuevo_habito)
                habitos.append(nuevo_habito)
            session.commit()
            
            # Recuperar con IDs asignados
            habitos = session.query(Habito).filter(Habito.user_id == user_id).all()
        return habitos
    except Exception as e:
        session.rollback()
        print(f"[Database ERROR] Error al cargar/inicializar hábitos: {e}")
        return []
    finally:
        session.close()


def update_habit_status(user_id: int, nombre_habito: str, completado: bool) -> bool:
    """Actualiza el estado de un hábito y su racha asociada.
    
    También sincroniza el JSON del estado del entorno.
    """
    session = Session()
    try:
        # Buscar el hábito por nombre y usuario
        habito = session.query(Habito).filter(
            Habito.user_id == user_id,
            Habito.nombre == nombre_habito
        ).first()
        
        if not habito:
            print(f"[Database Warning] Hábito '{nombre_habito}' no encontrado para usuario {user_id}.")
            return False
            
        # Si el estado no cambia, no hacemos nada
        if habito.estado_actual == completado:
            return True
            
        # Actualizar estado y racha
        habito.estado_actual = completado
        if completado:
            habito.racha_actual += 1
        else:
            # Si se desmarca, se reinicia la racha para penalizar el incumplimiento
            habito.racha_actual = 0
            
        session.commit()
        
        # Sincronizar el estado del entorno virtual
        sincronizar_estado_entorno(session, user_id)
        return True
    except Exception as e:
        session.rollback()
        print(f"[Database ERROR] Error al actualizar estado del hábito '{nombre_habito}': {e}")
        return False
    finally:
        session.close()


def sincronizar_estado_entorno(session: SqlalchemySession, user_id: int):
    """Actualiza el registro JSON del entorno virtual en base al estado de los hábitos."""
    habitos = session.query(Habito).filter(Habito.user_id == user_id).all()
    entorno = session.query(EstadoEntorno).filter(EstadoEntorno.user_id == user_id).first()
    
    if not entorno:
        entorno = EstadoEntorno(user_id=user_id, habitacion_level=1, items_ordenados_json="{}")
        session.add(entorno)
    
    # Mapear estado
    items_estado = {
        "cama": "messy",
        "libros": "messy",
        "ropa": "messy"
    }
    
    for h in habitos:
        if h.nombre == "Tender la cama":
            items_estado["cama"] = "clean" if h.estado_actual else "messy"
        elif h.nombre == "Leer páginas de un libro":
            items_estado["libros"] = "clean" if h.estado_actual else "messy"
        elif h.nombre == "Ordenar la ropa":
            items_estado["ropa"] = "clean" if h.estado_actual else "messy"
            
    entorno.items_ordenados_json = json.dumps(items_estado)
    session.commit()


def get_dopamina_y_progreso(user_id: int) -> dict:
    """Calcula el progreso diario y los puntos de dopamina del usuario."""
    session = Session()
    try:
        habitos = session.query(Habito).filter(Habito.user_id == user_id).all()
        if not habitos:
            return {"dopamina": 100, "progreso_pct": 0, "progreso_val": 0.0, "estados": {}}
            
        completados = [h for h in habitos if h.estado_actual]
        total_habitos = len(habitos)
        
        progreso_val = len(completados) / total_habitos if total_habitos > 0 else 0.0
        progreso_pct = int(progreso_val * 100)
        
        # Calcular Puntos de Dopamina: Base 100 + 50 por hábito completado + 10 por cada día de racha acumulada
        dopamina = 100 + (len(completados) * 50) + sum(h.racha_actual * 10 for h in completados)
        
        estados = {}
        for h in habitos:
            if h.nombre == "Tender la cama":
                estados["cama"] = "Ordenada" if h.estado_actual else "Destendida"
            elif h.nombre == "Leer páginas de un libro":
                estados["libros"] = "Libros ordenados" if h.estado_actual else "Libros desordenados"
            elif h.nombre == "Ordenar la ropa":
                estados["ropa"] = "Silla despejada" if h.estado_actual else "Silla con ropa"
                
        return {
            "dopamina": dopamina,
            "progreso_pct": progreso_pct,
            "progreso_val": progreso_val,
            "estados": estados
        }
    except Exception as e:
        print(f"[Database ERROR] Error al calcular dopamina y progreso: {e}")
        return {"dopamina": 100, "progreso_pct": 0, "progreso_val": 0.0, "estados": {}}
    finally:
        session.close()


def save_focus_session(user_id: int, energia_pre: int, motivacion_pre: int, energia_post: int, motivacion_post: int, completado: bool) -> bool:
    """Registra una sesión de enfoque en el historial de dopamina."""
    session = Session()
    try:
        # Registrar sesión de enfoque
        nuevo_registro = HistorialDopamina(
            user_id=user_id,
            energia_pre=energia_pre,
            motivacion_pre=motivacion_pre,
            energia_post=energia_post,
            motivacion_post=motivacion_post,
            bloques_completados=1 if completado else 0
        )
        session.add(nuevo_registro)
        session.commit()
        print(f"[Database] Sesión de enfoque guardada con éxito (Completada={completado}).")
        return True
    except Exception as e:
        session.rollback()
        print(f"[Database ERROR] Error al guardar sesión de enfoque: {e}")
        return False
    finally:
        session.close()

