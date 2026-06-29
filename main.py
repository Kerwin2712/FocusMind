import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Cargar el archivo de diseño KV de manera explícita
Builder.load_file(os.path.join(os.path.dirname(__file__), 'ui', 'main.kv'))


class WelcomeScreen(Screen):
    """Pantalla de bienvenida inicial para FocusMind."""
    pass


class FocusMindApp(App):
    """Aplicación principal de FocusMind."""
    
    def build(self):
        # El ScreenManager gestiona la navegación entre las pantallas de la app
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        return sm


from database.connection import init_db

if __name__ == '__main__':
    # Inicializar la base de datos al arrancar la aplicación
    db_ok = init_db()
    if not db_ok:
        print("[Warning] La aplicación iniciará sin persistencia de datos funcional debido a un error crítico.")
    
    FocusMindApp().run()

