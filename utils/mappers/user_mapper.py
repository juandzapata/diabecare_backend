from schemas.notification import TokenDeviceOut
from data.models.base import TokenUsuario, Usuario
from schemas.user import GetUser
from utils.constants.default_values import NOT_ID


class UserMapper:

    @staticmethod
    def to_user_get_login(user: Usuario) -> GetUser:
        user_login = GetUser(
                usuarioId = user.usuarioId,
                nombre = user.nombre,
                apellidos = user.apellidos,
                correo = user.correo,
                contraseña = user.contraseña,
                sexo = user.sexo,
                ciudad = user.ciudad,
                foto = user.foto,
                fechaNacimiento = user.fechaNacimiento.__str__(),
                rolId = user.rolId
            )
        if user.rolId is not None:
            user_login.rolId = user.rolId
        return user_login
        

    @staticmethod
    def to_user_token_out(token: TokenUsuario) -> TokenDeviceOut:
       return TokenDeviceOut(
            usuarioId=token.usuarioId,
            tokenDispositivo=token.tokenDispositivo,
            tokenUsuarioId=token.tokenUsuarioId
        )