from models.base import Usuario
from schemas.usuario import GetUsuario


def todos_los_usuarios(db) -> list[GetUsuario]:
    result = []
    usuarios = db.query(Usuario).all()
    for usuario in usuarios:
        try:
            result.append(GetUsuario(
            id=usuario.usuarioId,
            nombre=usuario.nombre,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            contrasena=usuario.contraseña,
            sexo=usuario.sexo,
            ciudad=usuario.ciudad,
            foto=usuario.foto,
            fecha_nacimiento=usuario.fechaNacimiento,
        ))
        except Exception as e:
            print(e)
            continue
    return result