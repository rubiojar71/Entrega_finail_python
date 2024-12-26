import sqlite3
import os,time
from colorama import Fore, Style, init

# Inicializar Colorama
init(autoreset=True)

# Nombre de la base de datos
DB_NAME = 'inventario.db'


def clear_screen():
    # Comando para limpiar la pantalla según el sistema operativo
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para macOS y Linux
        os.system('clear')
        
def pausa():
    if os.name == 'nt':  # Windows
        os.system('pause')
    else:  # macOS y Linux
        input("Presione una tecla para continuar...")

def espera():
    time.sleep(1) 
    os.system('cls')

# Diccionario de datos
diccionario_datos = {
    "productos": {
        "id": {
            "tipo": "INTEGER",
            "restricciones": ["PRIMARY KEY", "AUTOINCREMENT"],
            "descripcion": "Identificador único del producto."
        },
        "nombre": {
            "tipo": "TEXT",
            "restricciones": ["NOT NULL"],
            "descripcion": "Nombre del producto."
        },
        "descripcion": {
            "tipo": "TEXT",
            "restricciones": [],
            "descripcion": "Breve descripción del producto."
        },
        "cantidad": {
            "tipo": "INTEGER",
            "restricciones": ["NOT NULL"],
            "descripcion": "Cantidad disponible del producto."
        },
        "precio": {
            "tipo": "REAL",
            "restricciones": ["NOT NULL"],
            "descripcion": "Precio unitario del producto."
        },
        "categoria": {
            "tipo": "TEXT",
            "restricciones": [],
            "descripcion": "Categoría a la que pertenece el producto."
        }
    }
}

# Crear la base de datos y la tabla si no existen
def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Mostrar el diccionario de datos
def mostrar_diccionario():
    print(Fore.CYAN + "Diccionario de Datos:")
    for tabla, campos in diccionario_datos.items():
        print(Fore.BLUE + f"\nTabla: {tabla}")
        for campo, detalles in campos.items():
            print(f"  Campo: {campo}")
            print(f"    Tipo: {detalles['tipo']}")
            print(f"    Restricciones: {', '.join(detalles['restricciones']) if detalles['restricciones'] else 'Ninguna'}")
            print(f"    Descripción: {detalles['descripcion']}")

# Registrar un nuevo producto
def registrar_producto():
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    #cantidad = int(input("Cantidad: "))    
    cantidad = 0
    while cantidad < 1:
        try:
            cantidad = int(input("Cantidad: "))    
            if cantidad < 1:
                print(Fore.RED + "DATO INVÁLIDO ❌. La cantidad debe ser mayor o igual a 1.")
        except ValueError:
            print(Fore.RED + "DATO INVÁLIDO ❌. Ingrese un número entero.")
   
        precio = 0
    
    while precio <=0:
        try:
            precio = input("Precio: ")
            precio=float(precio.replace(',', '.'))
            if precio <=0:
                print("Ingrese un numero mayor que 0")
        except ValueError:
            print("Ingrese un numero")
            precio = 0

    categoria = input("Categoría: ").capitalize()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "Producto registrado con éxito.")
    pausa()    

# eliminar todos los productos
def eliminar_producto():
    mostrar_productos()  # Mostrar todos los productos para que el usuario pueda seleccionar
    try:
        id_producto = int(input("Ingrese el ID del producto a eliminar: "))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        if producto:
            # Confirmar eliminación
            confirmar = input(Fore.YELLOW + f"¿Está seguro que desea eliminar el producto '{producto[1]}'? (s/n): ").lower()
            if confirmar == 's':
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                conn.commit()
                print(Fore.GREEN + "Producto eliminado con éxito.")
            else:
                print(Fore.CYAN + "Operación cancelada.")
        else:
            print(Fore.RED + "No se encontró un producto con ese ID.")
        conn.close()
    except ValueError:
        print(Fore.RED + "El ID debe ser un número.")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")



# Actualizar un producto por id
def actualizar_producto():
    mostrar_productos()  # Mostrar todos los productos para que el usuario seleccione uno
    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: "))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        if producto:
            print(Fore.YELLOW + f"Producto seleccionado: {producto[1]} (ID: {producto[0]})")
            print(Fore.CYAN + "Deje en blanco para mantener el valor actual.\n")
            
            # Solicitar nuevos valores
            nuevo_nombre = input(f"Nombre actual ({producto[1]}): ") or producto[1]
            nueva_descripcion = input(f"Descripción actual ({producto[2]}): ") or producto[2]
            nueva_cantidad = input(f"Cantidad actual ({producto[3]}): ") or producto[3]
            nuevo_precio = input(f"Precio actual ({producto[4]}): ") or producto[4]
            nueva_categoria = input(f"Categoría actual ({producto[5]}): ") or producto[5]

            # Actualizar en la base de datos
            cursor.execute('''
                UPDATE productos
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            ''', (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria, id_producto))
            
            conn.commit()
            print(Fore.GREEN + "Producto actualizado con éxito.")
        else:
            print(Fore.RED + "No se encontró un producto con ese ID.")
        conn.close()
    except ValueError:
        print(Fore.RED + "El ID debe ser un número.")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")

def reporte_bajo_stock():
    # Límite de stock considerado como "bajo"
    limite_stock = 0
    while limite_stock <= 0:
        try:
            limite_stock = int(input("Ingrese la cantidad mínima permitida: "))
            if limite_stock <= 0:
                print(Fore.RED + "❌ Ingrese un número mayor que 0.")
        except ValueError:
            print(Fore.RED + "❌ Entrada inválida. Ingrese un número válido.")
            limite_stock = 0
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()        
        # Consultar productos con stock menor al límite
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite_stock,))
        productos = cursor.fetchall()
        conn.close()
        
        if productos:
            print(Fore.YELLOW + f"\nProductos con bajo stock (menos o igual de {limite_stock} unidades):")            
            print(Fore.CYAN + f"{'ID':<5}{'Nombre':<20}{'Descripción':<30} {'Cantidad':>10}{'Precio':>10} {'Categoría':>10}")
            print(Fore.CYAN + "-" * 90)
            for prod in productos:                
                print(f"{prod[0]:<5}{prod[1]:<20}{prod[2]:<30}{prod[3]:>10}{prod[4]:>10}  {prod[5]:>10}")
        else:
            print(Fore.GREEN + "Todos los productos tienen stock suficiente.")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error al generar el reporte: {e}")

# Mostrar todos los productos
def mostrar_productos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()    
    if productos:
        print("\n## Productos ✅ ##")            
        print(Fore.CYAN + f"{'ID':<5}{'Nombre':<20}{'Descripción':<30} {'Cantidad':>10}{'Precio':>10} {'Categoría':>10}")
        print(Fore.CYAN + "-" * 90)
        for prod in productos:            
            print(f"{prod[0]:<5}{prod[1]:<20}{prod[2]:<30}{prod[3]:>10}{prod[4]:>10}  {prod[5]:>10}")
            
    else:
        print(Fore.YELLOW + "No hay productos registrados.")
    pausa()


def buscar_productos_por_nombre():
    nombre_producto = input("Ingrese el nombre del producto a buscar: ")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    with conn as conexion:        
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre_producto}%",))
        resultados = cursor.fetchall()
        if resultados:
            print("\n## Productos encontrados ✅ ##")            
            print(Fore.CYAN + f"{'ID':<5}{'Nombre':<20}{'Descripción':<30} {'Cantidad':>10}{'Precio':>10} {'Categoría':>10}")
            print("-" * 90)
            for prod in resultados:                                
                print(f"{prod[0]:<5}{prod[1]:<20}{prod[2]:<30}{prod[3]:>10}{prod[4]:>10}  {prod[5]:>10}")
        else:
            print(Fore.RED + f"❌ No se encontraron productos con el nombre '{nombre_producto}'.")


# Mostrar solo un  producto        
def consultar_Inventario():
    try:
        # Pedir al usuario el ID del producto que desea consultar
        id_producto = int(input("Ingrese el ID del producto a consultar: "))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Buscar el producto en la base de datos
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        conn.close()
        
        if producto:
            # Mostrar la información del producto
            print(Fore.CYAN + f"\nInformación del Producto (ID: {producto[0]})")
            print(Fore.CYAN + f"Nombre: {producto[1]}")
            print(Fore.CYAN + f"Descripción: {producto[2]}")
            print(Fore.CYAN + f"Cantidad Disponible: {producto[3]}")
            #print(Fore.CYAN + f"Precio: ${producto[4]:.2f}")
            #print(Fore.CYAN + f"Categoría: {producto[5]}")
        else:
            print(Fore.RED + "No se encontró un producto con ese ID.")
    except ValueError:
        print(Fore.RED + "El ID debe ser un número.")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")


# Menú principal
def menu():
    
    inicializar_db()
    while True:     
        clear_screen()      
        print(Fore.BLUE + "\nMenú Principal")
        print("1. Alta de productos")        
        print("2. Modificar producto") 
        print("3. Eliminar producto")                 
        print("4. Reporte de todos los productos")
        print("5. Reporte de producto por nombre")                
        print("6. Consulta de inventario")         
        print("7. Reporte de bajo STOCK")  
        print("8. Mostrar diccionario de datos")         
        print("9. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":            
            registrar_producto()
            clear_screen()
        elif opcion == "2":            
            actualizar_producto()
            pausa()
            clear_screen()         
        elif opcion == "3":            
            eliminar_producto()
            pausa()
            clear_screen()  
        elif opcion == "4":            
            mostrar_productos()
            clear_screen()
        elif opcion == "5":            
            buscar_productos_por_nombre()    
            pausa()
            clear_screen()
        elif opcion == "6":            
            consultar_Inventario()
            pausa()
            clear_screen()                     
        elif opcion == "7":            
            reporte_bajo_stock()    
            pausa()
            clear_screen()     

        elif opcion == "8":            
            mostrar_diccionario()
            pausa()
            clear_screen()

        elif opcion == "9":            
            print(Fore.GREEN + "¡Gracias por usar la aplicación!")
            break
        else:
            print(Fore.RED + "La opción no válida.")
            espera()
        
            
# Ejecutar la aplicación
if __name__ == "__main__":    
    menu()
