from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from database.services import get_dopamina_y_progreso


class DashboardScreen(Screen):
    """Pantalla del entorno virtual interactivo (Dashboard) conectada a la base de datos."""
    
    # Propiedades reactivas de Kivy para enlazar dinámicamente con el main.kv
    dopamina_text = StringProperty("100 DP")
    progreso_text = StringProperty("Progreso diario: 0%")
    progreso_value = NumericProperty(0.0)
    habitacion_status_text = StringProperty("")
    
    # Propiedades booleanas para el renderizado interactivo del entorno
    cama_ordenada = BooleanProperty(False)
    libros_ordenados = BooleanProperty(False)
    ropa_ordenada = BooleanProperty(False)

    def on_enter(self):
        """Se ejecuta automáticamente al navegar al Dashboard."""
        self.update_dashboard_data()

    def update_dashboard_data(self):
        """Consulta la base de datos local y actualiza los indicadores del entorno."""
        # Obtener métricas calculadas y estados actuales de los hábitos
        data = get_dopamina_y_progreso(user_id=1)
        
        self.dopamina_text = f"{data['dopamina']} DP"
        self.progreso_text = f"Progreso diario: {data['progreso_pct']}%"
        self.progreso_value = data['progreso_val']
        
        estados = data['estados']
        cama = estados.get("cama", "Destendida")
        libros = estados.get("libros", "Libros desordenados")
        ropa = estados.get("ropa", "Silla con ropa")
        
        # Actualizar booleanos de renderizado condicional en la UI
        self.cama_ordenada = (cama == "Ordenada")
        self.libros_ordenados = (libros == "Libros ordenados")
        self.ropa_ordenada = (ropa == "Silla despejada")
        
        # Texto descriptivo para accesibilidad
        self.habitacion_status_text = (
            f"Cama: {cama}  |  Estante: {libros}  |  Ropa: {ropa}"
        )
