import csv
import requests
from PIL import Image
from obra import Obra
import io


class ManejadorDatos:
    """
    Clase para manejar la carga de datos de la API
    """

    def __init__(self):
        """
        Inicializa el manejador de datos
        """
        # Guardar la dirección URL de la API
        self.API = "https://collectionapi.metmuseum.org/public/collection/v1"
        # Inicializar listas para guardar los datos
        self.obras, self.departamentos, self.nacionalidades = [], [], []
        # Obtener los datos de la API y las nacionalidades
        self.obtener_obras()
        self.obtener_departamentos()
        self.obtener_nacionalidades()
        
    def obtener_departamentos(self):
        """
        Obtiene la lista de departamentos desde la API
        """
        try:
            respuesta = requests.get(f"{self.API}/departments")
            respuesta.raise_for_status()
            datos = respuesta.json()
            # Guardar departamentos disponibles en la lista
            for dept in datos.get('departments', []):
                self.departamentos_disponibles.append({'id': dept['departmentId'], 'nombre': dept['displayName']})
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener departamentos: {e}")

    def obtener_nacionalidades(self, archivo="./nacionalidades.csv"):
        # Cargar las nacionalidades disponibles desde el archivo
        self.nacionalidades_disponibles = []
        with open(archivo, "r") as f:
            lector = csv.reader(f)
            for fila in list(lector)[1:]:
                self.nacionalidades_disponibles.append(fila[0])
    
    def obtener_obras_por_departamento(self, id_departamento):
        """
        Obtiene obras de arte por departamento
        """
        try:
            # Obtener IDs de obras en el departamento
            respuesta = requests.get(f"{self.API}/objects?departmentIds={id_departamento}")
            respuesta.raise_for_status()
            ids_objetos = respuesta.json().get('objectIDs', [])[:50]  # Limitar a 50 para demo
            # Obtener detalles de cada obra
            for id_obj in ids_objetos:
                obra = self.obtener_obra(id_obj)
                if obra:
                    self.obras.append(obra)
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener obras por departamento: {e}")
    
    def obtener_obra(self, id_objeto):
        """
        Obtiene detalles de una obra específica
        """
        try:
            respuesta = requests.get(f"{self.API}/objects/{id_objeto}")
            respuesta.raise_for_status()
            datos = respuesta.json()
            # Preparar diccionario con los datos de la obra
            datos_obra = {
                'id_obra': id_objeto,
                'titulo': datos.get('title', 'Sin título'),
                'nombre_artista': datos.get('artistDisplayName', 'Desconocido'),
                'nacionalidad': datos.get('artistNationality', 'Desconocida'),
                'año_nacimiento': datos.get('artistBeginDate', ''),
                'año_muerte': datos.get('artistEndDate', ''),
                'clasificacion': datos.get('classification', 'Desconocido'),
                'fecha_obra': datos.get('objectDate', 'Desconocido'),
                'nombre_departamento': datos.get('department', 'Desconocido'),
                'url_imagen': datos.get('primaryImage', datos.get('additionalImages', [''])[0])
            }
            return Obra(datos_obra)
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener detalles de la obra {id_objeto}: {e}")
            return None
    
    def mostrar_imagen_obra(self, id_obra):
        """
        Muestra la imagen de una obra específica
        Args:
        id_obra (int): ID de la obra a buscar
        """
        obra = next((obra for obra in self.obras if obra.id == id_obra), None)
        if not obra or not obra.url_imagen:
            print("No se encontró la obra o no tiene imagen disponible.")
            return
        try:
            respuesta = requests.get(obra.url_imagen, stream=True)
            respuesta.raise_for_status()
            imagen = Image.open(io.BytesIO(respuesta.content))
            imagen.show()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la imagen: {e}")
        except Exception as e:
            print(f"Error al mostrar la imagen: {e}")
