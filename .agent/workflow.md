# CONTRATO DE INTERACCIÓN Y FLUJO DE TRABAJO

Antes de proceder con cualquier modificación de código, análisis o propuesta, debes leer y alinear tu comportamiento con las siguientes directrices mandatorias:

## 1. Gestión de Contexto y Documentación
- Revisa exhaustivamente la documentación del proyecto antes de proponer cambios en archivos `.py` o `.kv`.
- Es obligatorio mantener una bitácora de cambios actualizada. Cada modificación en el código debe quedar registrada de forma ordenada, cronológica y detallada en el archivo correspondiente.
- Es obligatorio mantener actualizado el archivo README.md de la raíz, reflejando el estado actual del proyecto, cómo ejecutarlo y su arquitectura a medida que evolucione.


## 2. Límites Operativos del Sistema (Restricciones Git y Entorno)
- **Commits:** Tienes permitido realizar commits locales de forma incremental para asegurar la trazabilidad de tus cambios.
- **Push:** Está estrictamente PROHIBIDO realizar `git push`. La subida al repositorio remoto queda bajo la total responsabilidad del usuario.
- **Pruebas y Navegación:** No abras el navegador web bajo ninguna circunstancia. El entorno de pruebas lo gestiona el usuario; ejecuta los cambios y espera el feedback del comportamiento de la UI de Kivy.

## 3. Estándares Técnicos y Arquitectura
- Mantén la arquitectura estrictamente desacoplada (separa por completo la lógica de negocio y base de datos de la capa de interfaz gráfica de Kivy).
- No agregues dependencias ni librerías externas que no hayan sido validadas explícitamente.

## 4. Directrices de Seguridad para Google Play Store
- Queda prohibido el uso de funciones de ejecución dinámica de código (`eval()`, `exec()`) que violen las políticas de comportamiento malicioso de Google Play.
- Toda persistencia local (SQLite) de tokens de sesión o datos sensibles del usuario debe implementarse pensando en el uso de capas seguras de almacenamiento, evitando archivos de texto plano desprotegidos.
- Las consultas SQL deben utilizar parametrización obligatoria (prohibida la concatenación directa de strings) para neutralizar vectores de inyección SQL.

Adopta un enfoque riguroso, crítico y de honestidad intelectual. Si una instrucción del usuario pone en riesgo la estabilidad de la UI de Kivy o viola las directrices de Google Play, adviértelo de inmediato antes de escribir código.
