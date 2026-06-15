class EventoAcceso:
    """Representa un evento de acceso al sistema."""

    def __init__(self, fecha, usuario_id, metodo, ubicacion, estado):
        """Inicializa un evento de acceso."""
        self.fecha = fecha              # Cuándo ocurrió
        self.usuario_id = usuario_id    # Quién fue
        self.metodo = metodo            # Cómo ingresó (QR, tarjeta, etc)
        self.ubicacion = ubicacion      # Dónde ocurrió
        self.estado = estado            # Si fue permitido o denegado

    def to_dict(self):
        """Convierte el evento a diccionario para enviar por API."""
        return {
            "fecha": self.fecha,
            "usuario_id": self.usuario_id,
            "metodo": self.metodo,
            "ubicacion": self.ubicacion,
            "estado": self.estado
        }