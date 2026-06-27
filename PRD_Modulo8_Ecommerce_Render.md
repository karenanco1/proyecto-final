# Product Requirement Document (PRD)
## Módulo 8: Entrega Final de E-Commerce & Despliegue

| Atributo | Detalle |
| :--- | :--- |
| **Proyecto** | E-Commerce MVP Final |
| **Estado** | Listo para Desarrollo / Despliegue |
| **Audiencia** | Portafolio Técnico (GitHub) |
| **Stack Principal** | Django, Django ORM, SQLite3, Bootstrap, Render |

---

## 1. Propósito y Objetivos
El objetivo de este módulo es consolidar e integrar las funcionalidades desarrolladas en los módulos anteriores en una aplicación web e-commerce completamente funcional, estable y lista para producción.

### Objetivos Clave:
* **Estabilidad del Core:** Asegurar que el flujo principal (*Catálogo → Carrito → Checkout*) funcione sin errores.
* **Listo para Portafolio:** Código limpio, repositorio de GitHub organizado y documentación clara para reclutadores.
* **Despliegue Exitoso:** Aplicación accesible públicamente en **Render** utilizando SQLite3 como persistencia simplificada.

---

## 2. Alcance del MVP (Módulo por Módulo)

### 2.1 Autenticación y Control de Accesos
Sistema de usuarios basado en el modelo nativo de Django, dividiendo la experiencia en dos roles principales:

* **Cliente:**
    * Registro e Inicio de sesión (Login/Logout).
    * Acceso exclusivo a la persistencia de su propio carrito y generación de órdenes.
* **Administrador (Staff):**
    * Inicio de sesión.
    * Acceso restringido a las vistas de gestión de productos (CRUD).
    * *Nota:* Se deben proteger estas vistas mediante decoradores `@login_required` y `@user_passes_test` o mixins equivalentes.

### 2.2 Catálogo y Persistencia (Django ORM)
* **Base de datos:** SQLite3 (tanto en local como en Render).
* **Modelos requeridos:** `Producto` (Nombre, descripción, precio, stock, imagen/url).
* **Acciones del Admin:** Crear, leer, actualizar y eliminar (CRUD) productos directamente desde la interfaz del frontend (además del `/admin` nativo).

### 2.3 Carrito de Compras y Flujo de Checkout
El núcleo transaccional de la aplicación debe cumplir con el siguiente flujo:
`[Catálogo] ──> [Añadir al Carrito] ──> [Gestionar Cantidades] ──> [Confirmar Compra (Orden)]`

* **Operaciones del Carrito:**
    * Agregar productos (validando que no exceda el stock si se controla, o sumando de 1 en 1).
    * Eliminar productos por completo del carrito.
    * Modificar cantidades directamente con validación de números enteros positivos ($> 0$).
    * Cálculo en tiempo real de subtotales por ítem y el Gran Total de la compra.
* **Confirmación de Compra (Checkout):**
    * Al hacer clic en "Confirmar Compra", se debe generar un registro en el modelo `Orden` (Pedido) y `ItemOrden` en la base de datos.
    * La orden debe quedar asociada al usuario que inició sesión.
    * Vaciar el carrito automáticamente tras el éxito de la operación.

### 2.4 Vistas y Navegación (Frontend)
Diseño consistente utilizando **Bootstrap**. La navegación debe ser intuitiva mediante un Navbar dinámico:
* **Navbar Público/Cliente:** Catálogo | Carrito (con contador de ítems) | Login o Logout (según estado).
* **Navbar Admin:** Gestión de Productos | Ir al Catálogo | Logout.
* **Mensajes de Feedback:** Integrar `django.contrib.messages` para mostrar alertas flotantes de Bootstrap (Ej: *"Producto añadido al carrito"*, *"Compra realizada con éxito"*, *"Error: El precio debe ser mayor a 0"*).

---

## 3. Especificaciones Técnicas de Despliegue (Render)

Para desplegar en Render con **SQLite3** de manera persistente (evitando que los productos se borren cada vez que el servidor se reinicie), utilizaremos un **Disco de Almacenamiento Persistente (Persistent Volume)**.

No se utilizará archivo `render.yaml`, la configuración se hará directamente en el dashboard de Render.

### 3.1 Archivos de Configuración Requeridos

#### 1. `requirements.txt`
Asegúrate de incluir las dependencias necesarias para producción:
```text
Django>=4.2,<5.1
gunicorn
whitenoise
```

#### 2. `Procfile` (En la raíz del proyecto)
Archivo sin extensión que le dice a Render cómo arrancar la aplicación:
```text
web: gunicorn tu_proyecto.wsgi:application
```

#### 3. Script de construcción: `build.sh` (En la raíz del proyecto)
Script para automatizar la preparación del entorno en cada despliegue.
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos
python manage.py migrate
```
> **Nota:** Recuerda darle permisos de ejecución al script antes de subirlo a GitHub con el comando: `chmod +x build.sh`

---

### 3.2 Modificación Crítica en `settings.py`

Para que Render guarde la base de datos en el disco persistente y use `whitenoise` para los archivos estáticos (Bootstrap, CSS, JS), edita tu `settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-de-desarrollo')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# 2. Configuración de Archivos Estáticos (WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Añadir justo debajo de SecurityMiddleware
    # ... demás middlewares
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 3. Base de Datos persistente en Render
# Si estamos en Render, usamos la ruta del volumen persistente (/data/)
if 'RENDER' in os.environ:
    DB_PATH = os.path.join('/data', 'db.sqlite3')
else:
    DB_PATH = BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
    }
}
```

---

### 3.3 Pasos para el Despliegue en el Dashboard de Render

1. **Crear un nuevo servicio:** Ve a Render → **New +** → **Web Service**.
2. **Conectar repositorio:** Vincula tu cuenta de GitHub y selecciona el repositorio de este proyecto.
3. **Configuración Básica:**
   * **Runtime:** `Python3`
   * **Build Command:** `./build.sh`
   * **Start Command:** `gunicorn tu_proyecto.wsgi:application` (o lo que configuraste en tu `Procfile`).
4. **Configurar Variables de Entorno (Advanced):**
   * Añade `PYTHON_VERSION` = `3.10.x` (o la versión que uses).
   * Añade `SECRET_KEY` = `UnTextoMuyLargoYAlAzarParaProduccion`.
   * Añade `RENDER` = `True`.
5. **Añadir Disco Persistente (CRÍTICO para SQLite3):**
   * En la misma sección avanzada, busca **Disks** → **Add Disk**.
   * **Name:** `sqlite-disk`
   * **Mount Path:** `/data`
   * **Size:** `1 GiB` (Suficiente para el MVP de portafolio y entra en el plan gratis).

---

## 4. Criterios de Aceptación para Portafolio (Definición de Hecho)
El entregable se considerará completado exitosamente cuando:
1. **Cero caídas en el flujo:** Un usuario anónimo puede loguearse, añadir 2 productos, modificar la cantidad de uno, ver el total correcto y clickear "Confirmar" generando la orden sin errores 500.
2. **Seguridad básica:** Si un cliente intenta entrar a `/productos/crear/` de forma manual en la URL, el sistema lo redirige al login o le da un error 403.
3. **Persistencia tras reinicio:** Si editas un producto en Render, fuerzas un redeploy (reinicio de servidor), el producto modificado **sigue existiendo** gracias al volumen `/data`.
4. **README en GitHub:** El repositorio cuenta con un archivo `README.md` que explica brevemente el proyecto, cómo ejecutarlo en local (`pip install`, `migrate`, `runserver`) y el enlace directo a la aplicación corriendo en Render.
