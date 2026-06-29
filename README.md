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

## 🔒 Directrices de Seguridad para Google Play Store
FocusMind incorpora medidas críticas para cumplir con las políticas de distribución de Google Play:
1.  **Prevención de SQLi:** SQLAlchemy gestiona las consultas de forma parametrizada nativamente, neutralizando vectores de inyección SQL.
2.  **Cifrado en Tránsito:** Las llamadas al backend remoto PostgreSQL requieren HTTPS/TLS obligatorio.
3.  **Sandbox Seguro:** El archivo SQLite local se almacena en el espacio de almacenamiento privado del sistema operativo Android, aislado de otras aplicaciones.
4.  **Cumplimiento de Políticas:** No se utiliza ejecución dinámica de código (`eval()`, `exec()`) que pueda violar las políticas de comportamiento malicioso.
