class EventoAcceso:

    def __init__(self, fecha, usuario_id, metodo, ubicacion, estado):

        self.fecha = fecha
        self.usuario_id = usuario_id
        self.metodo = metodo
        self.ubicacion = ubicacion
        self.estado = estado


    def to_dict(self):

        return {

            "fecha": self.fecha,
            "usuario_id": self.usuario_id,
            "metodo": self.metodo,
            "ubicacion": self.ubicacion,
            "estado": self.estado

        }