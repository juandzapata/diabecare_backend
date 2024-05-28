from data.models.base import Usuario
from schemas.user import GetUser


def todos_los_usuarios(db) -> list[GetUser]:
    result = []
    usuarios = db.query(Usuario).all()
    for usuario in usuarios:
        try:
            result.append(GetUser(
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