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


if __name__ == '__main__':
    FocusMindApp().run()
