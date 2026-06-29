from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, BooleanProperty, StringProperty


class FMButton(ButtonBehavior, Label):
    """Botón personalizado estilizado con propiedades reactivas."""
    bg_color = ListProperty([0.11, 0.11, 0.18, 1])
    radius = ListProperty([12])


class FMCheckBox(ButtonBehavior, BoxLayout):
    """Checkbox personalizado con soporte para textos y estados interactivos."""
    active = BooleanProperty(False)
    text = StringProperty("")
    subtext = StringProperty("")
