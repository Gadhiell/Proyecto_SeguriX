from data.memory_db import usuarios


class UsuarioRepository:
    """Maneja todas las operaciones con usuarios."""

    def obtener_todos(self):
        """Retorna lista de todos los usuarios."""
        try:
            return list(usuarios.values())
        except Exception as e:
            print(f"Error obteniendo usuarios: {e}")
            return []

    def obtener_por_id(self, usuario_id):
        """Busca un usuario por su ID."""
        try:
            return usuarios.get(str(usuario_id))
        except Exception as e:
            print(f"Error buscando usuario: {e}")
            return None

    def agregar(self, usuario):
        """Guarda un nuevo usuario."""
        try:
            usuarios[str(usuario["id"])] = usuario
            return True
        except Exception as e:
            print(f"Error agregando usuario: {e}")
            return False

    def total_usuarios(self):
        """Cuenta cuántos usuarios hay."""
        try:
            return len(usuarios)
        except Exception:
            return 0

    def total_activos(self):
        """Cuenta usuarios activos."""
        try:
            return sum(
                1 for usuario in usuarios.values()
                if usuario.get("activo", False)
            )
        except Exception:
            return 0

    def buscar_por_nombre(self, nombre):
        """Busca usuarios por nombre (sin importar mayúsculas)."""
        try:
            nombre_lower = nombre.lower()
            return [
                u for u in usuarios.values()
                if nombre_lower in u.get("nombre", "").lower()
            ]
        except Exception as e:
            print(f"Error buscando por nombre: {e}")
            return []

    def actualizar(self, usuario_id, datos):
        """Modifica datos de un usuario."""
        try:
            usuario_id_str = str(usuario_id)
            if usuario_id_str not in usuarios:
                return False

            usuarios[usuario_id_str].update(datos)
            return True
        except Exception as e:
            print(f"Error actualizando usuario: {e}")
            return False

    def eliminar(self, usuario_id):
        """Borra un usuario."""
        try:
            usuario_id_str = str(usuario_id)
            if usuario_id_str in usuarios:
                del usuarios[usuario_id_str]
                return True
            return False
        except Exception as e:
            print(f"Error eliminando usuario: {e}")
            return False
