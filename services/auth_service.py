def validar_acceso(usuario_id, usuarios):
    usuario = usuarios.get(usuario_id)

    if not usuario:
        return False, "inactivo"

    if not usuario["activo"]:
        return False, "inactivo"

    return True, "activo"