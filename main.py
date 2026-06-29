import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Registrar widgets personalizados en Python antes de que Kivy lea el archivo KV
from ui.custom_widgets import FMButton, FMCheckBox

# Cargar el archivo de diseño KV de manera explícita
Builder.load_file(os.path.join(os.path.dirname(__file__), 'ui', 'main.kv'))



# Importar pantallas del módulo ui
from ui import WelcomeScreen, DashboardScreen, HabitsScreen, FocusScreen


class FocusMindApp(App):
    """Aplicación principal de FocusMind."""
    
    def build(self):
        # El ScreenManager de Kivy maneja las transiciones del flujo
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(HabitsScreen(name='habits'))
        sm.add_widget(FocusScreen(name='focus'))
        return sm

    def change_screen(self, screen_name):
        """Cambia de pantalla gestionando de forma inteligente la dirección del deslizamiento."""
        if not self.root:
            return
            
        screen_order = {
            'welcome': -1,
            'dashboard': 0,
            'habits': 1,
            'focus': 2
        }
        
        current_name = self.root.current
        current_idx = screen_order.get(current_name, 0)
        target_idx = screen_order.get(screen_name, 0)
        
        if target_idx > current_idx:
            self.root.transition.direction = 'left'
        else:
            self.root.transition.direction = 'right'
            
        self.root.current = screen_name




from database.connection import init_db

if __name__ == '__main__':
    # Inicializar la base de datos al arrancar la aplicación
    db_ok = init_db()
    if not db_ok:
        print("[Warning] La aplicación iniciará sin persistencia de datos funcional debido a un error crítico.")
    
    FocusMindApp().run()

