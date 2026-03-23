from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Importamos el esquema que creamos en el Punto 3 (suponiendo que está en schema.py)
from .schema import schema

# 1. Inicializamos la aplicación FastAPI
app = FastAPI(title="Mi API de Tareas con Firebase y GraphQL")

# 2. Creamos el enrutador de GraphQL pasándole nuestro esquema
graphql_app = GraphQLRouter(schema)

# 3. Añadimos el enrutador a FastAPI en la ruta "/graphql"
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def raiz():
    return {"mensaje": "Bienvenido a la API. Visita /graphql para hacer consultas."}