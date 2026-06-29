# FocusMind - Neuroproductividad y Hábitos Gamificados

FocusMind es una aplicación móvil diseñada para optimizar la gestión de hábitos y la neuroproductividad utilizando mecánicas de gamificación basadas en la neurociencia del comportamiento (regulación de la dopamina). Mediante la visualización de un entorno virtual interactivo que evoluciona u ordena según las metas cumplidas, los usuarios pueden mejorar su enfoque diario.

---

## 🚀 Características Clave

*   **Core de Dopamina:** Gamificación integrada basada en rachas (streaks), objetivos diarios y bloques de enfoque con penalizaciones por incumplimiento (deterioro del entorno).
*   **Modelo Freemium Adaptativo:**
    *   *Gratuito (Online):* Sincronización directa con PostgreSQL en la nube, uso de bloques limitados (1.5 usos diarios) y visualización de anuncios.
    *   *Premium (Offline):* Funcionamiento local 100% independiente utilizando una base de datos local SQLite, sin anuncios y acceso ilimitado.
*   **Registro de Telemetría Cognitiva:** Registro analítico pre y post bloque de enfoque para evaluar los niveles de energía y motivación.

---

## 🛠️ Stack Tecnológico

*   **Lenguaje:** Python 3.9+
*   **Framework UI:** Kivy (2.2.0+)
*   **Persistencia Local:** SQLite3 (a través de SQLAlchemy)
*   **Persistencia Cloud:** PostgreSQL (a través de pg8000 & SQLAlchemy)
*   **Empaquetado Móvil:** Buildozer (dirigido a la plataforma Android)

---

## 📂 Arquitectura del Proyecto

El código está estructurado bajo un patrón desacoplado y modular para separar la interfaz gráfica de Kivy de la lógica de negocio y base de datos:

```text
FocusMind/
├── .agent/               # Documentación técnica del proyecto y workflow del agente
├── assets/               # Recursos gráficos y fuentes de la aplicación
│   ├── fonts/            # Fuentes tipográficas personalizadas (ej: Outfit)
│   └── images/           # Texturas del entorno virtual (Habitación, Oficina, etc.)
├── database/             # Lógica de datos y persistencia (Modelos ORM y conexión)
│   ├── connection.py     # Manejo de conexión híbrida SQLite / PostgreSQL
│   └── models.py         # Declaración de modelos SQLAlchemy (Usuarios, Habitos, etc.)
├── ui/                   # Interfaz de usuario (Layouts de Kivy)
│   ├── __init__.py       # Inicialización y exportación de pantallas
│   ├── dashboard_screen.py # Pantalla del entorno virtual interactivo
│   ├── focus_screen.py   # Pantalla del temporizador de enfoque
│   ├── habits_screen.py  # Pantalla del listado de hábitos (hoja de papel)
│   ├── main.kv           # Estilos KV y navegación compartida (NavBar)
│   └── welcome_screen.py # Pantalla de bienvenida y control de acceso

├── CHANGELOG.md          # Bitácora de cambios detallada y cronológica
├── main.py               # Punto de entrada de la aplicación
└── requirements.txt      # Dependencias del sistema
```

---

## ⚙️ Configuración y Ejecución

### 1. Requisitos Previos
Asegúrate de tener instalado Python (versión 3.9 a 3.13) en tu sistema de desarrollo.

### 2. Crear y Activar el Entorno Virtual
En tu terminal (PowerShell en Windows), ejecuta:
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\activate
```

### 3. Instalar Dependencias
Instala los paquetes necesarios desde `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto. Si deseas utilizar el backend PostgreSQL en la nube (Modo Free), define la variable `DATABASE_URL`:
```env
DATABASE_URL=postgresql+pg8000://usuario:contraseña@host:puerto/nombre_bd
```
*Nota: Si no se define `DATABASE_URL` en el entorno, la aplicación iniciará automáticamente en **Modo Premium/Offline** utilizando la base de datos SQLite local `focusmind.db`.*

### 5. Ejecutar la Aplicación
Inicia FocusMind ejecutando:
```powershell
python main.py
```

---

## 🔄 Flujo de Datos y Persistencia (Fase 3)
La aplicación implementa un patrón completamente desacoplado (MVVM/MVC adaptativo) para el manejo de estados entre la interfaz gráfica (Kivy) y la base de datos:

1.  **Capa de Presentación (UI):** Las pantallas `DashboardScreen` y `HabitsScreen` se enlazan de forma reactiva mediante `Properties` de Kivy (`StringProperty`, `NumericProperty`, `BooleanProperty`).
2.  **Capa de Servicios (`database/services.py`):** Encapsula todas las operaciones de base de datos. La UI nunca ejecuta consultas directas ni importa sesiones de SQLAlchemy.
3.  **Persistencia y Entorno Reactivo:**
    *   Al marcar un checkbox de hábito, se actualiza `estado_actual` y `racha_actual` en la tabla `Habitos` de SQLite/Postgres.
    *   La actualización recalcula automáticamente el JSON de estados en `Estado_Entorno` (sincronizando los objetos de la habitación virtual: cama, libros, ropa).
    *   Al regresar al Dashboard, el cambio de pantalla (`on_enter`) gatilla la lectura de dopamina (DP) y progreso, renderizando condicionalmente el estado actual de los objetos (ej: "Cama: Ordenada" o "Cama: Destendida") y actualizando la barra de progreso.

---

## ⏱️ Arquitectura del Temporizador y Clock (Fase 4)
El temporizador de enfoque utiliza una arquitectura reactiva no bloqueante basada en el planificador nativo de Kivy:

1.  **Hilos de Interfaz No Bloqueantes:** El uso de bucles de retardo tradicionales (`time.sleep`) congelaría la UI del dispositivo móvil. En su lugar, el sistema hace uso de `kivy.clock.Clock` mediante `Clock.schedule_interval(self.update_timer, 1)` para decrementar de forma segura la cuenta atrás en intervalos precisos de 1 segundo sobre el hilo principal.
2.  **Modales de Telemetría Cognitiva (`EvaluationPopup`):** Al presionar "Iniciar", se suspende el conteo y se presenta un modal para calificar el nivel de **Energía** y **Motivación** iniciales (Pre). Al completarse (conteo llega a cero) o al detenerse manualmente, se abre un segundo modal para calificar el estado final (Post).
3.  **Persistencia Transaccional del Historial:** Los resultados se persisten en la tabla `Historial_Dopamina` marcando la sesión como completada con éxito o interrumpida manualmente, permitiendo el posterior análisis estadístico de neuroproductividad.

---



## 🔒 Directrices de Seguridad para Google Play Store
FocusMind incorpora medidas críticas para cumplir con las políticas de distribución de Google Play:
1.  **Prevención de SQLi:** SQLAlchemy gestiona las consultas de forma parametrizada nativamente, neutralizando vectores de inyección SQL.
2.  **Cifrado en Tránsito:** Las llamadas al backend remoto PostgreSQL requieren HTTPS/TLS obligatorio.
3.  **Sandbox Seguro:** El archivo SQLite local se almacena en el espacio de almacenamiento privado del sistema operativo Android, aislado de otras aplicaciones.
4.  **Cumplimiento de Políticas:** No se utiliza ejecución dinámica de código (`eval()`, `exec()`) que pueda violar las políticas de comportamiento malicioso.
