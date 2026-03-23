import strawberry
from typing import Optional
from .firebase_conf import db # Importamos nuestra conexión del Punto 2


@strawberry.type
class Tarea:
    id: str                # Aquí guardaremos el ID del documento de Firestore
    titulo: str            # Un campo obligatorio
    completada: bool       # Otro campo obligatorio
    descripcion: Optional[str] = None  # Campo opcional (puede ser None en Firestore)
    

# app/schema.py (Añadir a continuación de las definiciones de tipos)

# 1. Input estricto para la Creación
@strawberry.input
class TareaInput:
    titulo: str
    completada: bool = False  # Establecemos un valor por defecto sensato
    descripcion: Optional[str] = None

# 2. Input laxo para la Actualización (Operación PATCH parcial)
# En una actualización, todos los campos deben ser opcionales, ya que el cliente
# podría desear alterar únicamente el estado 'completada' sin reenviar el título.
@strawberry.input
class ActualizarTareaInput:
    titulo: Optional[str] = None
    completada: Optional[bool] = None
    descripcion: Optional[str] = None

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

@strawberry.type
class Mutation:

    @strawberry.mutation
    def crear_tarea(self, datos: TareaInput) -> Tarea:
        # Strawberry nos facilita la conversión del objeto Input a un diccionario estándar
        datos_dict = strawberry.asdict(datos)

        # Ejecutamos la inserción en la colección raíz
        # .add() es una operación que devuelve una tupla: (timestamp_creacion, DocumentReference)
        hora_creacion, doc_ref = db.collection("tareas").add(datos_dict)

        # Instanciamos y devolvemos el objeto de respuesta, inyectando el ID generado
        return Tarea(id=doc_ref.id, **datos_dict)
    
schema = strawberry.Schema(query=Query)