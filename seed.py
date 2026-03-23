# seed.py
from app.firebase_conf import db

# 1. Definimos nuestras tareas con sus comentarios anidados
tareas_demo = [
    {
        "titulo": "Aprender FastAPI",
        "descripcion": "Revisar la documentación oficial y levantar el servidor.",
        "completada": True,
        "comentarios": [
            {"autor": "Profe", "texto": "La documentación de FastAPI es de las mejores."},
            {"autor": "Alumno_1", "texto": "Me costó un poco arrancar Uvicorn, pero solucionado."}
        ]
    },
    {
        "titulo": "Configurar Firebase",
        "descripcion": "Descargar el JSON de credenciales y conectar la base de datos.",
        "completada": True,
        "comentarios": [
            {"autor": "Profe", "texto": "¡Cuidado! Nunca subáis el archivo JSON a GitHub."}
        ]
    },
    {
        "titulo": "Integrar GraphQL con Strawberry",
        "descripcion": "Crear el schema.py con nuestros primeros Tipos y Queries.",
        "completada": False,
        "comentarios": [] # Esta tarea aún no tiene comentarios
    }
]

def inicializar_db():
    print("Iniciando la carga de tareas y comentarios en Firebase...")

    for tarea in tareas_demo:
        # Extraemos la lista de comentarios y la sacamos de los datos de la tarea
        comentarios = tarea.pop("comentarios")

        # 2. Creamos la Tarea en Firebase
        doc_ref = db.collection("tareas").document()
        doc_ref.set(tarea)
        print(f"✅ Tarea creada: {tarea['titulo']} (ID: {doc_ref.id})")

        # 3. Guardamos los comentarios en su subcolección correspondiente
        for comentario in comentarios:
            doc_ref.collection("comentarios").document().set(comentario)

        if comentarios:
            print(f"   -> Añadidos {len(comentarios)} comentarios.")

    print("🎉 ¡Base de datos de Tareas inicializada con éxito!")

if __name__ == "__main__":
    inicializar_db()