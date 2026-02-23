# 📦 QR Generator Pro — v1.0.0

### Lanzamiento Inicial Estable

Se presenta la primera versión estable de **QR Generator Pro**, una aplicación de escritorio para generación y lectura de códigos QR diseñada con arquitectura modular, pruebas automatizadas y enfoque en estabilidad y mantenibilidad.

---

## 🚀 Highlights de la versión 1.0.0

### 🎯 Interfaz y Experiencia de Usuario (UX)
* **DPI Awareness nativo**: Escalado perfecto en monitores 1080p, 2K y 4K.
* **Invisibilidad Atómica**: Eliminación total de parpadeos y "ventanas fantasma" en el arranque y cuadros de diálogo.
* **Drag & Drop Inteligente**: Feedback visual en tiempo real (animación de icono, hover de fondo y tipografía dinámica).
* **Icono Profesional**: Uso de `.ico` multi-resolución para nitidez máxima en Windows.

---

### 📦 Distribución y Seguridad
* **Instalador Oficial**: Generado con Inno Setup (`QR_Generator_Setup.exe`).
* **Firma Digital**: Tanto el ejecutable principal como el instalador están firmados digitalmente (Editor: **Walter Pablo Tellez Ayala**).
* **Certificado Público**: Se incluye `Walter_Pablo_Tellez_Ayala_CodeSigning.cer` para verificar la confianza en entornos corporativos.

---

### 🧠 Motor de Procesamiento

#### 🔹 Generación

* Escalado dinámico según densidad de datos.
* Soporte completo para texto Unicode.
* Exportación en alta resolución sin pérdida de legibilidad.

#### 🔹 Lectura

* Detección robusta basada en OpenCV.
* Compatibilidad con imágenes rotadas o con ruido moderado.
* Manejo seguro de rutas con caracteres especiales (Unicode).

---

### 🌍 Internacionalización (i18n)

Soporte nativo para 9 idiomas:

* Español
* Inglés
* Alemán
* Francés
* Italiano
* Japonés
* Portugués
* Ruso
* Chino

La aplicación detecta el idioma del sistema o utiliza la configuración almacenada.

---

### 🏗️ Calidad de Ingeniería

* Arquitectura **MVC desacoplada**.
* Inyección de dependencias en controladores.
* Manejo de excepciones tipadas.
* Sistema de logging estructurado.
* Control seguro de concurrencia en procesos asíncronos.
* Suite de tests automatizados (Core + Controller).
* CI automático en GitHub Actions (Windows runner).

Esta versión alcanza:

* Cobertura global superior al 80%.
* Core cercano al 90%.
* Validación de flujos críticos del controlador.

---

## 🛠️ Requisitos del Sistema

* **OS**: Windows 10/11 (recomendado), compatible con Linux/macOS.
* **Python**: 3.10 o superior.

---

## 📦 Instalación

### Desde código fuente

```bash
git clone https://github.com/Pablitus666/QR-Generator.git
cd QR-Generator
pip install -r requirements.txt
python -m QRApp.main
```

---

## 🧪 Testing

Para ejecutar la suite de pruebas:

```bash
pip install -r requirements-dev.txt
pytest
```

---

## 👨‍💻 Autor

Desarrollado por **Walter Pablo Tellez Ayala**
Proyecto estructurado con estándares profesionales de arquitectura, testing y mantenimiento continuo.

---

## 🐞 Soporte

Para reportar errores o solicitar mejoras, abrir un *Issue* en el repositorio oficial.
