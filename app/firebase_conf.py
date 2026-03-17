import firebase_admin
from firebase_admin import credentials, firestore

# Vinculamos el archivo JSON de credenciales
cred = credentials.Certificate("serviceAccountKey.json")

# Inicializamos la App de Firebase (Solo una vez en todo el ciclo de vida)
firebase_admin.initialize_app(cred)

# Instanciamos el cliente de Firestore
db = firestore.client()