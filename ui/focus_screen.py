from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from database.services import save_focus_session

# Constante de sesión de enfoque (25 minutos en segundos)
SESSION_DURATION_SECONDS = 1500


class EvaluationPopup(Popup):
    """Popup de autoevaluación interactiva pre/post sesión."""
    
    def __init__(self, title_text, on_confirm_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = title_text
        self.size_hint = (0.85, 0.5)
        
        # Eliminar bordes, texturas nativas y estilizar cabecera
        self.background = ""
        self.background_color = [0.11, 0.11, 0.18, 1]  # #1D1D2F
        self.separator_height = 0  # Remover la línea del título
        self.title_align = 'center'
        self.title_size = '16sp'
        self.title_color = [0.95, 0.96, 0.96, 1]
        self.auto_dismiss = False

        
        self.on_confirm = on_confirm_callback
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Slider Energía (1-5)
        layout.add_widget(Label(text="Nivel de Energía (1-5)", font_size='14sp', bold=True))
        self.slider_energia = Slider(min=1, max=5, value=3, step=1)
        self.lbl_energia = Label(text="3", font_size='16sp', size_hint_x=None, width='30dp')
        self.slider_energia.bind(value=self._update_lbl_energia)
        
        row_energia = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        row_energia.add_widget(self.slider_energia)
        row_energia.add_widget(self.lbl_energia)
        layout.add_widget(row_energia)
        
        # Slider Motivación (1-5)
        layout.add_widget(Label(text="Nivel de Motivación (1-5)", font_size='14sp', bold=True))
        self.slider_motivacion = Slider(min=1, max=5, value=3, step=1)
        self.lbl_motivacion = Label(text="3", font_size='16sp', size_hint_x=None, width='30dp')
        self.slider_motivacion.bind(value=self._update_lbl_motivacion)
        
        row_motivacion = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        row_motivacion.add_widget(self.slider_motivacion)
        row_motivacion.add_widget(self.lbl_motivacion)
        layout.add_widget(row_motivacion)
        
        # Botón Confirmar
        btn_confirmar = Button(
            text="Confirmar",
            size_hint_y=None,
            height='45dp',
            background_color=[0, 0, 0, 0],
            bold=True
        )
        
        with btn_confirmar.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            self.rect_color = Color(0.55, 0.36, 0.96, 1)  # #8B5CF6 Morado
            self.rect = RoundedRectangle(size=btn_confirmar.size, pos=btn_confirmar.pos, radius=[10])
            btn_confirmar.bind(pos=self._update_btn_rect, size=self._update_btn_rect)
            
        btn_confirmar.bind(on_release=self._on_confirm_click)
        layout.add_widget(btn_confirmar)
        
        self.content = layout
        
    def _update_lbl_energia(self, instance, value):
        self.lbl_energia.text = str(int(value))
        
    def _update_lbl_motivacion(self, instance, value):
        self.lbl_motivacion.text = str(int(value))
        
    def _update_btn_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def _on_confirm_click(self, instance):
        self.dismiss()
        self.on_confirm(int(self.slider_energia.value), int(self.slider_motivacion.value))


class FocusScreen(Screen):
    """Pantalla de temporizador y persistencia de métricas cognitivas."""
    
    # Propiedades Kivy vinculadas reactivamente con ui/main.kv
    timer_text = StringProperty("25:00")
    seconds_remaining = NumericProperty(SESSION_DURATION_SECONDS)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False
        self.clock_event = None
        
        # Almacenamiento temporal de métricas iniciales (Pre)
        self.energia_pre = 3
        self.motivacion_pre = 3

    def start_timer(self):
        """Inicia el temporizador de enfoque.
        
        Si es una sesión nueva, requiere autoevaluación Pre-enfoque.
        """
        if self.is_running:
            return
            
        # Si ya estábamos en medio de una sesión pausada, reanudamos de inmediato sin volver a calificar el inicio
        if self.seconds_remaining < SESSION_DURATION_SECONDS:
            self._start_clock()
            return
            
        # Sesión nueva: abrir Popup de evaluación de inicio
        popup = EvaluationPopup(
            title_text="Autoevaluación: Estado Inicial (Pre)",
            on_confirm_callback=self._on_pre_evaluation_confirm
        )
        popup.open()

    def _on_pre_evaluation_confirm(self, energia, motivacion):
        """Callback ejecutado al confirmar el estado de ánimo inicial."""
        self.energia_pre = energia
        self.motivacion_pre = motivacion
        print(f"[Focus] Métricas Pre guardadas: Energía={energia}, Motivación={motivacion}")
        self._start_clock()

    def _start_clock(self):
        """Activa el temporizador de Kivy programado a intervalos de 1 segundo."""
        self.is_running = True
        self.clock_event = Clock.schedule_interval(self.update_timer, 1)

    def pause_timer(self):
        """Detiene temporalmente el conteo sin perder el progreso ni registrar métricas."""
        if not self.is_running:
            return
            
        if self.clock_event:
            Clock.unschedule(self.clock_event)
            
        self.is_running = False
        print("[Focus] Temporizador pausado.")

    def stop_timer(self):
        """Detiene el temporizador y solicita métricas Post-sesión como interrupción."""
        if self.seconds_remaining == SESSION_DURATION_SECONDS:
            return  # No hay sesión activa que detener
            
        self.pause_timer()
        
        # Sesión interrumpida: abrir Popup Post-sesión
        popup = EvaluationPopup(
            title_text="Autoevaluación: Sesión Interrumpida (Post)",
            on_confirm_callback=self._on_post_evaluation_interrupted_confirm
        )
        popup.open()

    def _on_post_evaluation_interrupted_confirm(self, energia, motivacion):
        """Callback al calificar una sesión que fue interrumpida manualmente."""
        # Guardar en base de datos indicando que el bloque no fue completado
        save_focus_session(
            user_id=1,
            energia_pre=self.energia_pre,
            motivacion_pre=self.motivacion_pre,
            energia_post=energia,
            motivacion_post=motivacion,
            completado=False
        )
        self.reset_timer()

    def update_timer(self, dt):
        """Resta un segundo al temporizador y actualiza la UI."""
        if self.seconds_remaining > 0:
            self.seconds_remaining -= 1
            # Convertir segundos a formato MM:SS
            minutos = int(self.seconds_remaining // 60)
            segundos = int(self.seconds_remaining % 60)
            self.timer_text = f"{minutos:02d}:{segundos:02d}"
        else:
            # El tiempo llegó a cero: Completado con éxito
            self.pause_timer()
            popup = EvaluationPopup(
                title_text="¡Bloque de Enfoque Completado! (Post)",
                on_confirm_callback=self._on_post_completed_confirm
            )
            popup.open()

    def _on_post_completed_confirm(self, energia, motivacion):
        """Callback ejecutado al confirmar el estado final tras completar la sesión."""
        # Guardar en base de datos indicando bloque completado con éxito
        save_focus_session(
            user_id=1,
            energia_pre=self.energia_pre,
            motivacion_pre=self.motivacion_pre,
            energia_post=energia,
            motivacion_post=motivacion,
            completado=True
        )
        self.reset_timer()

    def reset_timer(self):
        """Restablece el temporizador al valor por defecto (25 minutos)."""
        self.seconds_remaining = SESSION_DURATION_SECONDS
        self.timer_text = "25:00"
        self.is_running = False
        if self.clock_event:
            Clock.unschedule(self.clock_event)
        print("[Focus] Temporizador restablecido.")
