import uuid
from fastapi import FastAPI, Form, UploadFile, File
import os
import shutil

# creamos el servidor
app = FastAPI()

# definimos la ruta para registrar los usuarios
@app.post("/usuarios")
async def registrar_usuario(nombre: str = Form(...), direccion: str = Form(...), vip: bool = Form(False), fotografia: UploadFile = File(...)):
    print(f"Nombre: {nombre}")
    print(f"Dirección: {direccion}")
    print(f"VIP: {vip}")

    # creamos las carpetas de destino para el estado vip
    home_usuario = os.path.expanduser("~")
    carpeta_destino = os.path.join(home_usuario, "fotos-usuarios-vip" if vip else "fotos-usuarios")
    os.makedirs(carpeta_destino, exist_ok=True)

    # guardamos la foto con un nombre unico
    nombre_archivo = f"{uuid.uuid4()}{os.path.splitext(fotografia.filename)[1]}"
    ruta_foto = os.path.join(carpeta_destino, nombre_archivo)
    
    print(f"Guardando la fotografia en: {ruta_foto}")
    with open(ruta_foto, "wb") as buffer:
        shutil.copyfileobj(fotografia.file, buffer)

    # respuesta
    respuesta = {
        "nombre": nombre,
        "direccion": direccion,
        "vip": vip,
        "ruta_foto": ruta_foto
    }
    return respuesta

# la ruta de prueba
@app.get("/")
def inicio():
    print("Ruta / invocada")
    return {"mensaje": "Bienvenido a la API de registro de usuarios"}
