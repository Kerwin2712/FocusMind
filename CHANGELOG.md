# Bitácora de Cambios - FocusMind

Este archivo registra de manera cronológica y detallada todas las modificaciones, inicializaciones y avances realizados en el proyecto FocusMind.

---

## [1.0.0] - 2026-06-29

### Añadido
- **Estructura de Documentación (.agent/):**
  - Creada la carpeta `.agent/` con los siguientes documentos técnicos y de negocio:
    - `PRD.md`: Documento de Requisitos de Producto y especificaciones de gamificación.
    - `TRD.md`: Requisitos del sistema, arquitectura híbrida (SQLite/Postgres) y guías de seguridad de Play Store.
    - `UI_UX.md`: Guías de estilo de Kivy y assets interactivos para la habitación virtual.
    - `Flujo.md`: Recorrido lógico detallado del usuario según plan (Free vs. Premium).
    - `Backend.md`: Esquema unificado compatible con SQLite y PostgreSQL.
    - `Plan.md`: Roadmap estructurado de 6 fases de construcción.
    - `workflow.md`: Contrato de interacción obligatorio para la codificación.
- **Fase 1 - Inicialización del Entorno de Desarrollo:**
  - Archivo `requirements.txt` con las dependencias base (`kivy`, `SQLAlchemy` y el driver de PostgreSQL `pg8000`).
  - Estructura limpia de directorios:
    - `/assets/images/` para recursos de la habitación/entorno.
    - `/assets/fonts/` para tipografías premium.
    - `/database/` para los modelos de datos SQLAlchemy y lógica de conexión.
    - `/ui/` para archivos `.kv` e interfaz gráfica.
  - Archivo principal `main.py` con una app básica de Kivy cargando el layout principal desde `ui/main.kv` e inicializando la base de datos de manera segura al arrancar.
  - Archivo `ui/main.kv` definiendo la pantalla de bienvenida (`WelcomeScreen`) con la paleta de colores premium de FocusMind.
- **Fase 1 - Modelos de Datos y Conexión Híbrida:**
  - Archivo `database/models.py` conteniendo los modelos ORM de SQLAlchemy (`Usuario`, `Habito`, `HistorialDopamina`, `EstadoEntorno`) alineados con la especificación `Backend.md`.
  - Archivo `database/connection.py` que implementa la conexión dinámica a PostgreSQL (vía `DATABASE_URL` en `.env`) o fallback robusto a SQLite local (`focusmind.db`), junto con la carga manual del archivo `.env` para evitar dependencias innecesarias.
  - Nueva regla de documentación agregada a `.agent/workflow.md` para garantizar la actualización del `README.md`.
  - Rediseño profesional del `README.md` de la raíz detallando arquitectura, stack, ejecución y seguridad.
- **Fase 2 - UI Básica de Kivy y Navegación:**
  - Creados archivos individuales de pantalla en la carpeta `ui/`:
    - `welcome_screen.py`: Pantalla de bienvenida.
    - `dashboard_screen.py`: Pantalla principal del entorno virtual (Habitación).
    - `habits_screen.py`: Pantalla de hábitos (diseño tipo hoja de papel con checkboxes).
    - `focus_screen.py`: Pantalla del temporizador de enfoque (reloj y botones de control).
  - Actualizado `ui/__init__.py` para exportar las 4 pantallas del módulo.
  - Modificado `main.py` para registrar las pantallas en el `ScreenManager`.
  - Rediseñado completamente `ui/main.kv` agregando estilos detallados, el widget de barra de navegación reutilizable `NavBar` y botones de transición del flujo.


