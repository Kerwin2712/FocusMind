# PRD - Documento de Requisitos de Producto (Product Requirement Document)

## 1. Visión General de FocusMind
**FocusMind** es una aplicación móvil diseñada para la gestión de hábitos y la neuroproductividad gamificada. El objetivo principal es ayudar a los usuarios a construir hábitos sostenibles y mejorar su enfoque diario utilizando mecánicas basadas en la neurociencia del comportamiento, específicamente la regulación de la dopamina. A través de la visualización de un entorno virtual interactivo que evoluciona o se deteriora según las acciones del usuario, la aplicación transforma la autodisciplina en un juego de rol de la vida real.

---

## 2. Core de Gestión de Dopamina y Gamificación

El sistema de FocusMind está estructurado en torno al refuerzo positivo y negativo inmediato para modelar la conducta del usuario mediante mecánicas de dopamina controladas.

### 2.1. Métricas de Comportamiento
*   **Rachas (Streaks):** Contador de días consecutivos cumpliendo un hábito. Multiplica los puntos de experiencia y dopamina virtual obtenidos.
*   **Objetivos Diarios:** Tareas concretas y acotadas que definen el éxito del día.
*   **Bloques de Enfoque:** Sesiones de trabajo estructuradas (estilo Pomodoro, pero flexibles) orientadas a tareas de alta concentración.

### 2.2. Sistema de Recompensas y Entorno Virtual Evolutivo
*   **Puntos de Dopamina (DP):** Moneda virtual acumulada al completar hábitos y bloques de enfoque.
*   **Entorno Virtual Reactivo:** El progreso del usuario se visualiza en un entorno digital (habitación, oficina o casa).
    *   **Acciones Positivas:** Completar hábitos limpia y ordena el espacio (ej. tender la cama virtual, organizar el escritorio).
    *   **Evolución:** Los puntos permiten adquirir mejoras estéticas y funcionales para el entorno (muebles, decoraciones, plantas).

### 2.3. Penalizaciones por Incumplimiento
*   **Deterioro del Entorno:** Si el usuario no registra o marca como incumplidos sus hábitos diarios, el entorno virtual se desordena visiblemente (cama deshecha, basura digital en el suelo, luces opacas).
*   **Pérdida de Rachas:** No cumplir con el hábito en el periodo establecido reinicia el contador de racha, reduciendo temporalmente el multiplicador de DP.

### 2.4. Registro Analítico Pre/Post Bloque de Enfoque
Para medir el impacto de las sesiones de concentración, el usuario debe realizar una autoevaluación rápida antes y después de cada bloque de enfoque:
*   **Métricas de entrada (Pre-enfoque):** Nivel de energía (1-5) y Nivel de motivación (1-5).
*   **Métricas de salida (Post-enfoque):** Nivel de energía (1-5) y Nivel de motivación (1-5) alcanzados tras el bloque.
*   **Propósito:** Proporcionar al usuario gráficas e históricos de cómo el enfoque y el cumplimiento de hábitos modifican su estado energético y motivacional a lo largo del tiempo.

---

## 3. Modelo de Negocio Detallado (Freemium)

FocusMind implementa un modelo Freemium estrictamente definido por los siguientes límites y ventajas:

| Característica | Versión Gratuita (Free) | Versión Premium (Paga) |
| :--- | :--- | :--- |
| **Conectividad** | Requiere conexión online obligatoria. | Funciona 100% Offline (SQLite local independiente). |
| **Límite de Uso** | Límite diario de 1.5 usos/bloques de enfoque (máximo 1 sesión completa y otra parcial, regulado por slots de energía). | Uso ilimitado de bloques de enfoque y temporizadores. |
| **Gestión de Hábitos** | Acceso a pocos hábitos predefinidos básicos (ej. tender la cama, leer, ordenar ropa). | Creación ilimitada y personalización total de hábitos y rutinas. |
| **Soporte de Base de Datos** | Sincronización directa con base de datos remota (PostgreSQL). | Almacenamiento local aislado (SQLite) sin dependencias en la nube. |
| **Publicidad** | Anuncios no invasivos (Banners/Interstitials) entre bloques de enfoque. | Sin anuncios (Experiencia limpia e ininterrumpida). |
| **Gamificación** | Limitado al entorno inicial (Habitación básica). | Expansión del entorno a Casa completa, Oficina y jardines. |
