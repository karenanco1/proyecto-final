from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tienda.models import Producto, Orden, ItemOrden

PRODUCTOS = [
    {
        "nombre": "Laptop Gamer",
        "descripcion": "Laptop de alto rendimiento con GPU dedicada y 16GB RAM",
        "precio": 1200.00,
        "stock": 15,
        "imagen_url": "https://picsum.photos/seed/laptop/400/400",
    },
    {
        "nombre": "Auriculares Bluetooth",
        "descripcion": "Auriculares inalámbricos con cancelación de ruido",
        "precio": 89.99,
        "stock": 50,
        "imagen_url": "https://picsum.photos/seed/auriculares/400/400",
    },
    {
        "nombre": "Mesa de Escritorio",
        "descripcion": "Mesa moderna de 140cm con acabado de madera",
        "precio": 249.99,
        "stock": 20,
        "imagen_url": "https://picsum.photos/seed/mesa/400/400",
    },
    {
        "nombre": "Zapatillas Running",
        "descripcion": "Zapatillas ligeras con amortiguación avanzada",
        "precio": 129.99,
        "stock": 35,
        "imagen_url": "https://picsum.photos/seed/zapatillas/400/400",
    },
    {
        "nombre": "Camiseta Algodón",
        "descripcion": "Camiseta de algodón orgánico, corte regular",
        "precio": 24.99,
        "stock": 100,
        "imagen_url": "https://picsum.photos/seed/camiseta/400/400",
    },
    {
        "nombre": "Cafetera Eléctrica",
        "descripcion": "Cafetera programable de 12 tazas con jarra de vidrio",
        "precio": 79.99,
        "stock": 25,
        "imagen_url": "https://picsum.photos/seed/cafetera/400/400",
    },
    {
        "nombre": "Mochila Urbana",
        "descripcion": "Mochila impermeable con compartimento para laptop",
        "precio": 59.99,
        "stock": 40,
        "imagen_url": "https://picsum.photos/seed/mochila/400/400",
    },
    {
        "nombre": "Smartwatch Deportivo",
        "descripcion": "Reloj inteligente con GPS y monitor cardíaco",
        "precio": 199.99,
        "stock": 30,
        "imagen_url": "https://picsum.photos/seed/smartwatch/400/400",
    },
    {
        "nombre": "Silla Ergonómica",
        "descripcion": "Silla de oficina con soporte lumbar ajustable",
        "precio": 349.99,
        "stock": 12,
        "imagen_url": "https://picsum.photos/seed/silla/400/400",
    },
    {
        "nombre": "Parlante Portátil",
        "descripcion": "Parlante Bluetooth resistente al agua, 20h de batería",
        "precio": 49.99,
        "stock": 60,
        "imagen_url": "https://picsum.photos/seed/parlante/400/400",
    },
    {
        "nombre": "Reloj de Pared",
        "descripcion": "Reloj analógico clásico de 30cm de diámetro",
        "precio": 34.99,
        "stock": 45,
        "imagen_url": "https://picsum.photos/seed/reloj/400/400",
    },
    {
        "nombre": "Set de Sartenes",
        "descripcion": "Juego de 3 sartenes antiadherentes con tapa",
        "precio": 89.99,
        "stock": 28,
        "imagen_url": "https://picsum.photos/seed/sartenes/400/400",
    },
    {
        "nombre": "Pelota de Fútbol",
        "descripcion": "Balón oficial tamaño 5, cosido a máquina",
        "precio": 29.99,
        "stock": 55,
        "imagen_url": "https://picsum.photos/seed/pelota/400/400",
    },
    {
        "nombre": "Lámpara LED",
        "descripcion": "Lámpara de escritorio LED con brazo articulado",
        "precio": 44.99,
        "stock": 38,
        "imagen_url": "https://picsum.photos/seed/lampara/400/400",
    },
    {
        "nombre": "Cuaderno Profesional",
        "descripcion": "Cuaderno tapa dura, 200 hojas rayadas",
        "precio": 12.99,
        "stock": 80,
        "imagen_url": "https://picsum.photos/seed/cuaderno/400/400",
    },
    {
        "nombre": "Bolso de Cuero",
        "descripcion": "Bolso bandolera de cuero genuino, color marrón",
        "precio": 89.99,
        "stock": 22,
        "imagen_url": "https://picsum.photos/seed/bolso/400/400",
    },
    {
        "nombre": "Mouse Inalámbrico",
        "descripcion": "Mouse ergonómico con sensor óptico de 4000 DPI",
        "precio": 39.99,
        "stock": 65,
        "imagen_url": "https://picsum.photos/seed/mouse/400/400",
    },
    {
        "nombre": "Cojín Ergonómico",
        "descripcion": "Cojín lumbar de espuma viscoelástica",
        "precio": 54.99,
        "stock": 30,
        "imagen_url": "https://picsum.photos/seed/cojin/400/400",
    },
    {
        "nombre": "Taza Térmica",
        "descripcion": "Taza de acero inoxidable con tapa, 500ml",
        "precio": 19.99,
        "stock": 90,
        "imagen_url": "https://picsum.photos/seed/taza/400/400",
    },
    {
        "nombre": "Kit de Herramientas",
        "descripcion": "Kit de 40 piezas con caja organizadora",
        "precio": 69.99,
        "stock": 25,
        "imagen_url": "https://picsum.photos/seed/herramientas/400/400",
    },
]

USUARIOS = [
    {
        "username": "admin",
        "email": "admin@email.com",
        "password": "Admin123!",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "cliente1",
        "email": "cliente1@email.com",
        "password": "Cliente123!",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "cliente2",
        "email": "cliente2@email.com",
        "password": "Cliente123!",
        "is_staff": False,
        "is_superuser": False,
    },
]


class Command(BaseCommand):
    help = "Borra todos los datos existentes y siembra la base de datos con productos y usuarios de prueba"

    def handle(self, *args, **options):
        self.stdout.write("Limpiando base de datos...")

        ItemOrden.objects.all().delete()
        Orden.objects.all().delete()
        Producto.objects.all().delete()

        for usuario in USUARIOS:
            User.objects.filter(username=usuario["username"]).delete()

        self.stdout.write("Creando productos...")
        for prod in PRODUCTOS:
            Producto.objects.create(**prod)

        self.stdout.write(self.style.SUCCESS(f"  {len(PRODUCTOS)} productos creados"))

        self.stdout.write("Creando usuarios...")
        for data in USUARIOS:
            password = data.pop("password")
            user = User.objects.create_user(**data)
            user.set_password(password)
            user.save()

        self.stdout.write(self.style.SUCCESS("  Usuarios creados:"))
        for u in USUARIOS:
            self.stdout.write(f"    - {u['username']} ({u['email']})")

        self.stdout.write(self.style.SUCCESS("¡Seed completado exitosamente!"))
