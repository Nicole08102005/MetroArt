class Interfaz:
    """
    Clase para manejar la interfaz de usuario
    """
    
    def __init__(self, manejador_datos):
        """
        Inicializa la interfaz de usuario
        Args:
            manejador_datos (ManejadorDatos): Instancia del manejador de datos
        """
        self.manejador = manejador_datos
    
    def mostrar_menu_principal(self):
        """
        Muestra el menú principal y maneja la interacción del usuario
        """
        while True:
            print("--- CATÁLOGO METROART ---")
            print("Menú de opciones:")
            print("1. Buscar obras por departamento")
            print("2. Buscar obras por nacionalidad del autor")
            print("3. Buscar obras por nombre del autor")
            print("4. Salir")
            # Obtener la opción que desea realizar el usuario
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.buscar_por_departamento()
            elif opcion == "2":
                self.buscar_por_nacionalidad()
            elif opcion == "3":
                self.buscar_por_artista()
            elif opcion == "4":
                print("Gracias por usar MetroArt. ¡Hasta pronto!")
                print("Sesión finalizada.")
                break
            else:
                print("La opción ingresada no es válida. Por favor, intente nuevamente.")
    
    def buscar_por_departamento(self):
        """
        Maneja la búsqueda por departamento
        """
        if not self.manejador.departamentos_disponibles:
            print("No se pudieron cargar los departamentos. Por favor intente nuevamente.")
            return
        print("---")
        print("Departamentos disponibles:")
        for i, depto in enumerate(self.manejador.departamentos_disponibles, 1):
            print(f"{i}. {depto['nombre']}")
        while True:
            try:
                seleccion = int(input("Seleccione el número del departamento: "))
                # Verificar que el departamento seleccionado esté en el rango
                if 1 <= seleccion <= len(self.manejador.departamentos_disponibles):
                    id_depto = self.manejador.departamentos_disponibles[seleccion - 1]['id']
                    print("Cargando obras...")
                    # Mostrar obras si las hay
                    if self.manejador.obtener_obras_por_departamento(id_depto):
                        self.mostrar_obras(self.manejador.obras)
                        self.mostrar_detalles_obra()   
                    else:
                        print("No se encontraron obras en ese departamento.")
                    break
                # De lo contrario, seguir pidiendo un número de departamento
                else:
                    print("Selección no válida.")
            # Verificar que se haya ingresado un número entero
            except ValueError:
                print("Por favor ingrese un número válido.")
            
    def buscar_por_nacionalidad(self):
        """
        Maneja la búsqueda por nacionalidad
        """
        print("---")
        print("Nacionalidades disponibles:")
        for i, nacionalidad in enumerate(sorted(self.manejador.nacionalidades_disponibles), 1):
            print(f"{i}. {nacionalidad}")
        try:
            seleccion = int(input("Seleccione el número de la nacionalidad: "))
            nacionalidades_ordenadas = sorted(self.manejador.nacionalidades_disponibles)
            # Verificar que la nacionalidad seleccionada esté en el rango disponible
            if 1 <= seleccion <= len(nacionalidades_ordenadas):
                nacionalidad = nacionalidades_ordenadas[seleccion - 1]
                resultado = [obra for obra in self.obras if obra.nacionalidad.lower() == nacionalidad.lower()]
                if resultado:
                    self.mostrar_obras(resultado)
                    self.mostrar_detalles_obra()
                else:
                    print("No se encontraron obras para esta nacionalidad.")
            # De lo contrario, seguir pidiendo nacionalidad
            else:
                print("Selección no válida.")
        # Verificar que se haya ingresado un número entero
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    def buscar_por_artista(self):
        """
        Maneja la búsqueda por nombre de artista
        """
        print("---")
        # Obtener input de nombre del artista y buscar obras en base a ello
        nombre = input("Ingrese el nombre del artista (o parte del nombre): ")
        resultado = [obra for obra in self.obras if nombre.lower() in obra.artista.lower()]
        # Mostrar el resultado, si se consiguió
        if resultado:
            self.mostrar_obras(resultado)
            self.mostrar_detalles_obra()
        else:
            print("No se encontraron obras para este artista.")
    
    def mostrar_obras(self, obras):
        """
        Imprime la lista de obras encontradas para la búsqueda actual
        """
        print("---")
        print("Obras encontradas:")
        for obra in obras:
            print(obra.info_basica())
    
    def mostrar_detalles_obra(self):
        """
        Maneja la visualización de detalles de una obra específica
        """
        if not self.manejador.obras:
            print("No hay obras cargadas en el sistema.")
            return    
        while True:
            id_obra = input("Ingrese el ID de una obra para ver detalles (o '0' para volver): ")
            if id_obra == '0':
                break
            try:
                id_obra = int(id_obra)
                obra = next((obra for obra in self.manejador.obras if obra.id == id_obra), None)
                if obra:
                    print("Detalles de la obra:")
                    print(obra.info_completa())
                    # Mostrar imagen si se tiene una URL
                    if obra.url_imagen:
                        while True:
                            mostrar = input("¿Desea ver la imagen? (s/n): ").lower()
                            if mostrar == 's':
                                self.manejador.mostrar_imagen_obra(id_obra)
                                break
                            else:
                                print("Opción no válida. Intente de nuevo.")
                    else:
                        print("La obra seleccionada no tiene imagen disponible.")
                # Seguir pidiendo input hasta que se ingrese un ID válido
                else:
                    print("ID de obra no válido.")
            # Verificar que se haya ingresado un número entero
            except ValueError:
                print("Por favor ingrese un número válido.")
