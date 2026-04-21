from datetime import datetime
from app.config import db

leads = [
    {
        "nombre": "Juan Paz",
        "email": "juan2@example.com",
        "fuente": "instagram",
        "telefono": "3001234567",
        "producto_interes": "Tecnologia",
        "presupuesto": 1200,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "María Gómez",
        "email": "maria@example.com",
        "fuente": "facebook",
        "telefono": "3017654321",
        "producto_interes": "Hotel",
        "presupuesto": 800,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Jhon Rivas",
        "email": "jhon@example.com",
        "fuente": "instagram",
        "telefono": "3001234567",
        "producto_interes": "Paquete turístico",
        "presupuesto": 1200,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Andrea Paz",
        "email": "andrea@example.com",
        "fuente": "facebook",
        "telefono": "3017654321",
        "producto_interes": "Hotel",
        "presupuesto": 800,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Jaime Pinzon",
        "email": "jaime@example.com",
        "fuente": "instagram",
        "telefono": "3001234567",
        "producto_interes": "comida",
        "presupuesto": 1200,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Juliana Pinto",
        "email": "juliana@example.com",
        "fuente": "facebook",
        "telefono": "3017654321",
        "producto_interes": "Hotel",
        "presupuesto": 800,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Carla Mosquera",
        "email": "carla@example.com",
        "fuente": "instagram",
        "telefono": "3001234567",
        "producto_interes": "Paquete turístico",
        "presupuesto": 1200,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Eugenia Minota",
        "email": "eugenia@example.com",
        "fuente": "facebook",
        "telefono": "3017654321",
        "producto_interes": "Hotel",
        "presupuesto": 800,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    
]

db.leads.insert_many(leads)
print("Seed ejecutado: colección leads poblada con datos de ejemplo")
