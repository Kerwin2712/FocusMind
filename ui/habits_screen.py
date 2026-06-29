from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from database.services import get_user_habits, update_habit_status


class HabitsScreen(Screen):
    """Pantalla del listado y control de hábitos diarios con persistencia SQLite."""
    
    # Propiedades reactivas de Kivy para enlazar con la interfaz del archivo KV
    habito_cama_active = BooleanProperty(False)
    habito_libro_active = BooleanProperty(False)
    habito_ropa_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bandera de control para evitar llamadas redundantes a la BD durante la carga inicial
        self._loading = False

    def on_enter(self):
        """Se ejecuta automáticamente cuando el usuario navega a esta pantalla."""
        self.load_habits_data()

    def load_habits_data(self):
        """Carga el estado de los hábitos desde la base de datos."""
        self._loading = True
        habitos = get_user_habits(user_id=1)
        
        # Mapear los estados de la BD a las propiedades de la UI
        for habito in habitos:
            if habito.nombre == "Tender la cama":
                self.habito_cama_active = habito.estado_actual
            elif habito.nombre == "Leer páginas de un libro":
                self.habito_libro_active = habito.estado_actual
            elif habito.nombre == "Ordenar la ropa":
                self.habito_ropa_active = habito.estado_actual
        self._loading = False

    def on_habito_change(self, nombre_habito, active):
        """Manejador disparado cuando el usuario interactúa con un checkbox."""
        if self._loading:
            return
            
        print(f"[UI] Hábito '{nombre_habito}' cambiado a active={active}")
        # Actualizar en base de datos local
        success = update_habit_status(user_id=1, nombre_habito=nombre_habito, completado=active)
        if not success:
            print(f"[UI ERROR] No se pudo guardar el estado de '{nombre_habito}' en la base de datos.")
            # Revertir cambio en caso de error
            self.load_habits_data()
