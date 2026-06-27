# Proyecto Final - E-Commerce MVP

Aplicación web e-commerce desarrollada con Django como proyecto de portafolio.

## Requisitos Previos

- Python 3.10+
- pip
- virtualenv (recomendado)

## Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/karenanco1/proyecto-final.git
cd proyecto-final

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

## Seed de Datos de Prueba

Para poblar la base de datos con datos de ejemplo, ejecuta:

```bash
python manage.py seed
```

Este comando **borra todos los datos existentes** y los recrea desde cero.

### Usuarios de Prueba

| Rol | Username | Email | Contraseña |
|---|---|---|---|
| Administrador | `admin` | admin@email.com | Admin123! |
| Cliente | `cliente1` | cliente1@email.com | Cliente123! |
| Cliente | `cliente2` | cliente2@email.com | Cliente123! |

### Productos de Prueba (20)

| # | Producto | Precio | Stock |
|---|---|---|---|
| 1 | Laptop Gamer | $1,200.00 | 15 |
| 2 | Auriculares Bluetooth | $89.99 | 50 |
| 3 | Mesa de Escritorio | $249.99 | 20 |
| 4 | Zapatillas Running | $129.99 | 35 |
| 5 | Camiseta Algodón | $24.99 | 100 |
| 6 | Cafetera Eléctrica | $79.99 | 25 |
| 7 | Mochila Urbana | $59.99 | 40 |
| 8 | Smartwatch Deportivo | $199.99 | 30 |
| 9 | Silla Ergonómica | $349.99 | 12 |
| 10 | Parlante Portátil | $49.99 | 60 |
| 11 | Reloj de Pared | $34.99 | 45 |
| 12 | Set de Sartenes | $89.99 | 28 |
| 13 | Pelota de Fútbol | $29.99 | 55 |
| 14 | Lámpara LED | $44.99 | 38 |
| 15 | Cuaderno Profesional | $12.99 | 80 |
| 16 | Bolso de Cuero | $89.99 | 22 |
| 17 | Mouse Inalámbrico | $39.99 | 65 |
| 18 | Cojín Ergonómico | $54.99 | 30 |
| 19 | Taza Térmica | $19.99 | 90 |
| 20 | Kit de Herramientas | $69.99 | 25 |
