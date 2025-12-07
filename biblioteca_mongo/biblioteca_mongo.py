from pymongo import MongoClient
from bson.objectid import ObjectId

# -------------------------------------------
# CONEXIÓN A MONGODB
# -------------------------------------------

try:
    # Si usas MongoDB local
    client = MongoClient("mongodb://localhost:27017/")
    db = client["biblioteca"]
    coleccion = db["libros"]

    print("✔ Conexión exitosa a MongoDB.\n")

except Exception as e:
    print("❌ Error de conexión:", e)
    exit()


# -------------------------------------------
# FUNCIONES CRUD
# -------------------------------------------

def agregar_libro():
    titulo = input("Ingrese el título del libro: ")
    autor = input("Ingrese el autor del libro: ")
    genero = input("Ingrese el género del libro: ")
    estado = input("Estado del libro (leído/no leído): ")

    documento = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    try:
        coleccion.insert_one(documento)
        print("📌 Libro agregado exitosamente.\n")
    except Exception as e:
        print("❌ Error al agregar:", e)


def listar_libros():
    libros = list(coleccion.find())
    
    if libros:
        print("\n📚 Lista de libros registrados:")
        for libro in libros:
            print(f"ID: {libro['_id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Género: {libro['genero']} | Estado: {libro['estado']}")
        print()
    else:
        print("⚠ No hay libros registrados.\n")


def buscar_libros():
    criterio = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input(f"Ingrese el {criterio}: ")

    if criterio not in ["titulo", "autor", "genero"]:
        print("❌ Criterio inválido.\n")
        return

    filtro = {criterio: {"$regex": valor, "$options": "i"}}

    resultados = list(coleccion.find(filtro))

    if resultados:
        print("\n🔍 Resultados de búsqueda:")
        for libro in resultados:
            print(f"ID: {libro['_id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Género: {libro['genero']} | Estado: {libro['estado']}")
        print()
    else:
        print("⚠ No se encontraron coincidencias.\n")


def actualizar_libro():
    listar_libros()
    
    id_libro = input("Ingrese el ID del libro a actualizar: ")

    try:
        libro = coleccion.find_one({"_id": ObjectId(id_libro)})
    except:
        print("❌ ID inválido.\n")
        return

    if not libro:
        print("❌ Libro no encontrado.\n")
        return

    print("Deje en blanco si no desea modificar un campo.")
    nuevo_titulo = input("Nuevo título: ")
    nuevo_autor = input("Nuevo autor: ")
    nuevo_genero = input("Nuevo género: ")
    nuevo_estado = input("Nuevo estado (leído/no leído): ")

    cambios = {}

    if nuevo_titulo: cambios["titulo"] = nuevo_titulo
    if nuevo_autor: cambios["autor"] = nuevo_autor
    if nuevo_genero: cambios["genero"] = nuevo_genero
    if nuevo_estado: cambios["estado"] = nuevo_estado

    if cambios:
        try:
            coleccion.update_one({"_id": ObjectId(id_libro)}, {"$set": cambios})
            print("✔ Libro actualizado correctamente.\n")
        except Exception as e:
            print("❌ Error al actualizar:", e)
    else:
        print("⚠ No se realizaron cambios.\n")


def eliminar_libro():
    listar_libros()
    
    id_libro = input("Ingrese el ID del libro a eliminar: ")

    try:
        libro = coleccion.find_one({"_id": ObjectId(id_libro)})
    except:
        print("❌ ID inválido.\n")
        return

    if not libro:
        print("❌ Libro no encontrado.\n")
        return

    try:
        coleccion.delete_one({"_id": ObjectId(id_libro)})
        print("🗑 Libro eliminado correctamente.\n")
    except Exception as e:
        print("❌ Error al eliminar:", e)


# -------------------------------------------
# MENÚ PRINCIPAL
# -------------------------------------------

def menu():
    while True:
        print("📌 Menú de Biblioteca MongoDB")
        print("1. Agregar libro")
        print("2. Listar libros")
        print("3. Buscar libros")
        print("4. Actualizar libro")
        print("5. Eliminar libro")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            listar_libros()
        elif opcion == "3":
            buscar_libros()
        elif opcion == "4":
            actualizar_libro()
        elif opcion == "5":
            eliminar_libro()
        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("⚠ Opción inválida. Intente nuevamente.\n")


# Ejecutar sistema
menu()
