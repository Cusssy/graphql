import strawberry
from typing import Optional
from .firebase_conf import db # Importamos nuestra conexión del Punto 2


@strawberry.type
class Tarea:
    id: str                # Aquí guardaremos el ID del documento de Firestore
    titulo: str            # Un campo obligatorio
    completada: bool       # Otro campo obligatorio
    descripcion: Optional[str] = None  # Campo opcional (puede ser None en Firestore)
    
@strawberry.type
class Query:

    # Resolver para una sola tarea
    @strawberry.field
    def obtener_tarea(self, info: strawberry.Info, id_documento: str) -> Optional[Tarea]:
        # Accedemos a la colección en Firestore
        doc_ref = db.collection("tareas").document(id_documento)
        doc = doc_ref.get()

        if doc.exists:
            datos = doc.to_dict()
            # Unimos el ID con los datos del diccionario
            return Tarea(id=doc.id, **datos)

        return None

    # Resolver para la lista completa
    @strawberry.field
    def listar_tareas(self) -> list[Tarea]:
        docs = db.collection("tareas").stream()

        resultado = []
        for doc in docs:
            datos = doc.to_dict()
            # Convertimos cada documento NoSQL en un objeto Tarea
            resultado.append(Tarea(id=doc.id, **datos))

        return resultado