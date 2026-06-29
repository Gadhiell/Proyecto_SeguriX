class EventoAcceso:
    """Representa un evento de acceso."""

    def __init__(self, fecha, usuario_id, metodo, ubicacion, estado):
        """Inicializa un evento."""
        self.fecha = fecha  #fecha del evento
        self.usuario_id = usuario_id  #usuario involucrado
        self.metodo = metodo  #método usado
        self.ubicacion = ubicacion  #lugar del evento
        self.estado = estado  #resultado del acceso

    def to_dict(self):
        """Convierte el evento a dict para la API."""
        return {
            "fecha": self.fecha,
            "usuario_id": self.usuario_id,
            "metodo": self.metodo,
            "ubicacion": self.ubicacion,
            "estado": self.estado,
        }