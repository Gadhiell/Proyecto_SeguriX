def validar_acceso(usuario_id, usuarios):
    """
    Verifica si un usuario puede acceder.
    
    Retorna: (permitido: bool, estado: str)
    """
    try:
        # Buscar al usuario usando el ID como cadena para coincidir con las llaves en memoria
        usuario = usuarios.get(str(usuario_id))
        
        # Si no existe, no permitir
        if not usuario:
            return False, "inactivo"

        # Si no está activo, no permitir
        if not usuario.get("activo", False):
            return False, "inactivo"

        # Todo ok, permitir acceso
        return True, "activo"
        
    except Exception as e:
        print(f"Error validando acceso: {e}")
        return False, "inactivo"
