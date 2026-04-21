from app import create_app
from app.models import db, Activo, Amenaza, Salvaguarda, Riesgo, Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Base de datos inicializada correctamente.")

    # Usuario administrador
    admin = Usuario(
        username='admin',
        password=generate_password_hash('admin123')
    )
    db.session.add(admin)
    print("Usuario admin creado.")

    # Activos de Impresión Industrial Rioja
    activos_iniciales = [
        Activo(nombre='Servidor ERP', categoria='Servidor',
               disponibilidad=5, confidencialidad=4,
               integridad=5, autenticidad=3, trazabilidad=3,
               descripcion='Sistema ERP de gestión de producción y pedidos'),
        Activo(nombre='Base de datos corporativa', categoria='Datos',
               disponibilidad=5, confidencialidad=5,
               integridad=5, autenticidad=4, trazabilidad=4,
               descripcion='Base de datos principal del sistema ERP'),
        Activo(nombre='Servidor de archivos', categoria='Servidor',
               disponibilidad=4, confidencialidad=3,
               integridad=4, autenticidad=2, trazabilidad=2,
               descripcion='Almacenamiento de diseños y documentos'),
        Activo(nombre='Firewall perimetral', categoria='Red',
               disponibilidad=5, confidencialidad=3,
               integridad=4, autenticidad=3, trazabilidad=3,
               descripcion='Protección perimetral de la red corporativa'),
        Activo(nombre='NAS Backup', categoria='Almacenamiento',
               disponibilidad=4, confidencialidad=3,
               integridad=5, autenticidad=2, trazabilidad=3,
               descripcion='Sistema de copias de seguridad'),
    ]

    # Amenazas del catálogo MAGERIT
    amenazas_iniciales = [
        Amenaza(nombre='Fallo del sistema', tipo='Técnica',
                origen='Interno', probabilidad=3,
                descripcion='Interrupción por fallo de hardware o software'),
        Amenaza(nombre='Pérdida de datos', tipo='Técnica',
                origen='Interno', probabilidad=2,
                descripcion='Corrupción o pérdida de información crítica'),
        Amenaza(nombre='Ataque externo', tipo='Deliberada',
                origen='Externo', probabilidad=2,
                descripcion='Intrusión o ataque desde el exterior'),
        Amenaza(nombre='Ransomware', tipo='Deliberada',
                origen='Externo', probabilidad=2,
                descripcion='Cifrado malicioso de sistemas y datos'),
        Amenaza(nombre='Error humano', tipo='Accidental',
                origen='Interno', probabilidad=3,
                descripcion='Configuración incorrecta o borrado accidental'),
    ]

    for a in activos_iniciales:
        db.session.add(a)
    for a in amenazas_iniciales:
        db.session.add(a)

    db.session.commit()
    print(f"Cargados {len(activos_iniciales)} activos y "
          f"{len(amenazas_iniciales)} amenazas.")
    print("Inicialización completada. Accede con admin / admin123")
