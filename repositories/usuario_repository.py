from data.memory_db import usuarios


class UsuarioRepository:

    def obtener_todos(self):

        return list(
            usuarios.values()
        )


    def obtener_por_id(self, usuario_id):

        return usuarios.get(
            str(usuario_id)
        )


    def agregar(self, usuario):

        usuarios[
            str(usuario["id"])
        ] = usuario


    def total_usuarios(self):

        return len(
            usuarios
        )


    def total_activos(self):

        return sum(
            1
            for usuario in usuarios.values()
            if usuario.get("activo", False)
        )


    def buscar_por_nombre(self, nombre):

        nombre_lower = nombre.lower()
        return [
            u for u in usuarios.values()
            if nombre_lower in u.get("nombre", "").lower()
        ]


    def actualizar(self, usuario_id, datos):

        usuario_id_str = str(usuario_id)
        if usuario_id_str not in usuarios:
            return False

        usuarios[usuario_id_str].update(datos)
        return True


    def eliminar(self, usuario_id):

        usuario_id_str = str(usuario_id)
        if usuario_id_str in usuarios:
            del usuarios[usuario_id_str]
            return True
        return False