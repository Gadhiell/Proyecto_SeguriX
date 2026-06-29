from services.access_strategies import AccessValidationContext


_contexto_validacion = AccessValidationContext()


def validar_acceso(usuario_id, usuarios, metodo_solicitado=None):
    """Valida el acceso con la estrategia correspondiente."""
    try:
        usuario = usuarios.get(str(usuario_id))
        if usuario is None:
            return False, "inactivo"

        permitido, estado = _contexto_validacion.validate(usuario, metodo_solicitado)
        if estado == "activo":
            return True, estado

        return permitido, estado

    except Exception as e:
        print(f"Error validando acceso: {e}")
        return False, "inactivo"
