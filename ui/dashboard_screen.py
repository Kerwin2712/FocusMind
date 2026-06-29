from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from database.services import get_dopamina_y_progreso


class DashboardScreen(Screen):
    """Pantalla del entorno virtual interactivo (Dashboard) conectada a la base de datos."""
    
    # Propiedades reactivas de Kivy para enlazar dinámicamente con el main.kv
    dopamina_text = StringProperty("100 DP")
    progreso_text = StringProperty("Progreso diario: 0%")
    progreso_value = NumericProperty(0.0)
    habitacion_status_text = StringProperty("")

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
        
        # Renderizado condicional en formato texto explicativo del estado del entorno
        self.habitacion_status_text = (
            "[ Espacio de Render del Entorno ]\n\n"
            "El estado de la habitación refleja tus hábitos de hoy:\n"
            f"- Cama: {cama}\n"
            f"- Estantería: {libros}\n"
            f"- Ropa: {ropa}"
        )
