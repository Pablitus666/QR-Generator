# QR Generator Pro

![CI Status](https://github.com/Pablitus666/QR-Generator/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Architecture](https://img.shields.io/badge/Architecture-MVC-purple)
![Tests](https://img.shields.io/badge/Tests-32%20Passed-success)
![Coverage](https://img.shields.io/badge/Coverage-83%25-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Aplicación de escritorio profesional para **generación y lectura de códigos QR**, desarrollada en **Python** con arquitectura modular, testing automatizado y CI continuo.

## 📌 Descripción

QR Generator Pro es una aplicación desktop enfocada en:

*   **Generación Inteligente**: Crea códigos QR de alta densidad con escalado inteligente.
*   **Lectura Avanzada**: Soporte para arrastrar y soltar (Drag & Drop) imágenes locales.
*   **Interfaz Moderna**: UI intuitiva con tipografía "Inter" y tema oscuro profesional.

*   **Ingeniería Robusta**: Arquitectura desacoplada y testeable (MVC real)., inyección de dependencias y validación mediante tests automatizados.

El proyecto está diseñado siguiendo principios de ingeniería de software mantenible y escalable.

---

![QR Generator Preview](https://raw.githubusercontent.com/Pablitus666/QR-Generator/main/images/Preview.png)

---

## 🚀 Características

🔹**Generación Inteligente**
*   Ajuste dinámico de tamaño según la cantidad de datos.
*   Soporte completo para texto Unicode.
*   Exportación en alta resolución (PNG).

🔹**Lectura Avanzada**
*   **Drag & Drop Inteligente**: Animación de hover, escalado de icono y cambio de color de fondo en tiempo real.
*   **Detección Robusta**: Basada en OpenCV con manejo de ruido y rotación.
*   **Limpieza Automática**: Manejo de rutas con espacios y caracteres especiales (`{}`).

🔹**Interfaz Profesional e Ingeniería Visual**
*   **Invisibilidad Atómica**: Eliminación total de parpadeos y "ventanas fantasma" mediante opacidad controlada al inicio.
*   **Icono Hi-Res**: Uso nativo de archivos `.ico` multi-resolución para máxima nitidez en Windows.
*   **DPI Awareness**: Escalado nítido en monitores de alta resolución (DPI).
*   **Tema Oscuro**: Diseño moderno con tipografía "Inter".

🔹**Seguridad y Distribución**
*   **Firma Digital**: Ejecutable e instalador firmados con certificado profesional.
*   **Instalador Profesional**: Generado con Inno Setup, incluye desinstalador.
*   **Privacidad Total**: Procesamiento 100% local, sin conexión a internet.

🔹**Multilingüe**: Soporte nativo para 9 idiomas.

🔹**Ingeniería Robusta**
*   Arquitectura MVC real con inyección de dependencias.
*   Suite de tests automatizados con cobertura validada.
*   CI automático en GitHub Actions.

## 🏗️ Arquitectura
```
QRApp/
│
├── controllers/   # Orquestación y lógica de flujo
├── core/          # Lógica de negocio desacoplada
├── ui/            # Interfaz gráfica
├── utils/         # Utilidades auxiliares
├── locales/       # Archivos de traducción
├── logs/          # Registro de eventos
└── main.py        # Punto de entrada
```
Separación clara entre:

Lógica de negocio (Core)

Control de flujo (Controller)

Presentación (UI)

---

## 🛠️ Stack Tecnológico

*   **Lenguaje**: Python 3.10+
*   **GUI**: Tkinter + TkinterDnD2
*   **Core**: QRCode, OpenCV, Pillow
*   **Testing**: Pytest, Pytest-Cov
```
| Área                      | Tecnología            |
| ------------------------- | --------------------- |
| Lenguaje                  | Python 3.10+          |
| GUI                       | Tkinter + TkinterDnD2 |
| Generación QR             | qrcode                |
| Lectura QR                | OpenCV                |
| Procesamiento de imágenes | Pillow                |
| Testing                   | Pytest + Pytest-Cov   |
| CI                        | GitHub Actions        |
```
---
## 📦 Instalación y Ejecución

### Opción 1: Instalador (Recomendado)
Descarga el archivo `QR_Generator_Setup.exe` desde la sección de **[Releases](https://github.com/Pablitus666/QR-Generator/releases)** y sigue el asistente. El programa aparecerá en tu Menú Inicio y Escritorio.

### Opción 2: Desde código fuente
1️⃣ Clonar repositorio:
    ```bash
    git clone https://github.com/Pablitus666/QR-Generator.git
    cd QR-Generator
    ```

2️⃣ Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3️⃣ Ejecutar aplicación:
    ```bash
    python -m QRApp.main
    ```
---

## 📷 Capturas de pantalla

<p align="center">
  <img src="images2/screenshot.png?v=2" alt="Vista previa de la aplicación" width="600"/>
</p>

---

## ✅ Testing

El proyecto incluye pruebas unitarias para:

Módulos del Core
Controladores (con mocks)
Manejo de errores
Concurrencia básica

Ejecutar tests
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest
```
**Cobertura**

El proyecto mantiene una cobertura global superior al 80%, con:
Core cercano al 90%+
Validación de flujos críticos del Controller
CI ejecutando tests automáticamente en cada push

---
🔄 Integración Continua

Cada push al repositorio:

Ejecuta instalación limpia en entorno Windows.
Corre la suite completa de tests.
Verifica cobertura.
Falla el build si hay regresiones.
Esto garantiza estabilidad continua del proyecto.

📎 **Roadmap**
*   [x] Empaquetado distribuible (.exe).
*   [x] Firma digital del ejecutable e instalador.
*   [x] Mejoras visuales en micro-interacciones.
*   [ ] Soporte para códigos QR con logotipos.
*   [ ] Tests de integración end-to-end.

📜 **Licencia**

MIT License.

---

## 👨‍💻 Autor

**Walter Pablo Téllez Ayala**  
Software Developer

📍 Tarija, Bolivia <img src="https://flagcdn.com/w20/bo.png" width="20"/> <br>
📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com) 

© 2026 — QR - Generator

---

Desarrollado como proyecto de ingeniería de software con estándares profesionales de arquitectura, testing y mantenimiento continuo.

⭐ Si el proyecto te resulta útil, considera dejar una estrella en el repositorio.