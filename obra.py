class Obra:
    """Clase que representa una obra de arte del museo"""
    
    def __init__(self, datos_obra):
        """
        Inicializa una obra de arte con todos sus atributos
        
        Args:
            datos_obra (dict): Diccionario con todos los datos de la obra
        """
        self.id = datos_obra.get("id_obra", 0)
        self.titulo = datos_obra.get("titulo", 'Sin título')
        self.artista = datos_obra.get("nombre_artista", 'Desconocido')
        self.nacionalidad = datos_obra.get('nacionalidad', 'Desconocida')
        self.año_nacimiento = datos_obra.get('año_nacimiento', '')
        self.año_muerte = datos_obra.get('año_muerte', '')
        self.clasificacion = datos_obra.get("clasificacion", 'Desconocido')
        self.fecha_creacion = datos_obra.get("fecha_obra", 'Desconocido')
        self.departamento = datos_obra.get("nombre_departamento", 'Desconocido')
        self.url_imagen = datos_obra.get("url_imagen", '')
    
    def info_basica(self):
        """
        Devuelve información básica de la obra para listados
        """
        return f"ID: {self.id} - Título: {self.titulo} - Artista: {self.artista} - Creación {self.fecha_creacion}"
    
    def info_completa(self):
        """
        Devuelve información completa de la obra
        """
        return (
            f"Título: {self.titulo}"
            f"Artista: {self.artista}"
            f"Nacionalidad: {self.nacionalidad}"
            f"Fechas del artista: {self.año_nacimiento}-{self.año_muerte}"
            f"Tipo: {self.clasificacion}"
            f"Año de creación: {self.fecha_creacion}"
            f"Departamento: {self.departamento}"
            f"ID de la obra: {self.id}"
        )
