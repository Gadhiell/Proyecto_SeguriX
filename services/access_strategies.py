from abc import ABC, abstractmethod


class AccessStrategy(ABC):
    """Interfaz base para las estrategias de acceso."""

    @abstractmethod
    def authorize(self, usuario, metodo_solicitado):
        raise NotImplementedError

    def _coincide_con_metodo(self, usuario, metodo_solicitado, metodo_esperado):
        if not metodo_solicitado:
            return False
        metodo_usuario = normalizar_metodo(usuario.get("metodo")) if usuario else None
        return metodo_usuario == metodo_esperado and metodo_solicitado == metodo_esperado

    def _validar_estado(self, usuario):
        if not usuario:
            return False, "inactivo"
        if not usuario.get("activo", False):
            return False, "inactivo"
        return True, "activo"


class QrAccessStrategy(AccessStrategy):
    def authorize(self, usuario, metodo_solicitado):
        estado = self._validar_estado(usuario)
        if not estado[0]:
            return estado
        if not self._coincide_con_metodo(usuario, metodo_solicitado, "Código QR"):
            return False, "metodo_no_autorizado"
        return True, "activo"


class RfidAccessStrategy(AccessStrategy):
    def authorize(self, usuario, metodo_solicitado):
        estado = self._validar_estado(usuario)
        if not estado[0]:
            return estado
        if not self._coincide_con_metodo(usuario, metodo_solicitado, "Tarjeta RFID"):
            return False, "metodo_no_autorizado"
        return True, "activo"


class FingerprintAccessStrategy(AccessStrategy):
    def authorize(self, usuario, metodo_solicitado):
        estado = self._validar_estado(usuario)
        if not estado[0]:
            return estado
        if not self._coincide_con_metodo(usuario, metodo_solicitado, "Huella Digital"):
            return False, "metodo_no_autorizado"
        return True, "activo"


class DefaultAccessStrategy(AccessStrategy):
    def authorize(self, usuario, metodo_solicitado):
        estado = self._validar_estado(usuario)
        if not estado[0]:
            return estado
        return False, "metodo_no_soportado"


class AccessValidationContext:
    def __init__(self):
        self._strategies = {
            "Código QR": QrAccessStrategy(),
            "Tarjeta RFID": RfidAccessStrategy(),
            "Huella Digital": FingerprintAccessStrategy(),
        }
        self._default = DefaultAccessStrategy()

    def validate(self, usuario, metodo_solicitado):
        metodo = normalizar_metodo(metodo_solicitado)
        if not metodo:
            metodo = normalizar_metodo(usuario.get("metodo")) if usuario else None

        strategy = self._strategies.get(metodo, self._default)
        return strategy.authorize(usuario, metodo)


def normalizar_metodo(metodo_input):
    if not metodo_input:
        return None

    texto = str(metodo_input).strip().lower()

    if "qr" in texto:
        return "Código QR"
    if "tarjeta" in texto or "card" in texto or "rfid" in texto:
        return "Tarjeta RFID"
    if "huella" in texto or "finger" in texto:
        return "Huella Digital"

    return None
