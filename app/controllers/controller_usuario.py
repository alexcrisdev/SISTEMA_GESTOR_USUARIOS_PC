from flask import Blueprint, request, jsonify
from app.models.model_usuario import Usuario
from app.dao.dao_usuario import UsuarioDAO
from db.conexion_db import ConexionDB

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

conexion = ConexionDB()
usuario_dao = UsuarioDAO(conexion)

@usuario_bp.route('/', methods=['GET'])
def obtener_todos_usuarios():
    usuarios = usuario_dao.obtener_todos_usuario_DAO()
    if usuarios:
        return jsonify([u.to_dict() for u in usuarios]), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

@usuario_bp.route('/<id_usuario>', methods=['GET'])
def obtener_por_id_usuario(id_usuario):
    usuario = usuario_dao.obtener_usuario_por_id_DAO(id_usuario)
    if usuario:
        return jsonify(usuario.to_dict()), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

@usuario_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.get_json() #Convierte el JSON recibidio en un diccionario de Python
    try:
        nuevo_usuario = Usuario(**data) #Crear el objeto
        resultado = usuario_dao.insertar_usuario_DAO(nuevo_usuario)
        if resultado:
            return jsonify({'mensaje': 'Usuario insertado correctamente'}), 201
        else:
            return jsonify({'error': 'No se pudo insertar el usuario'}), 400
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 400
    
@usuario_bp.route('/lote', methods=['POST'])
def crear_usuarios_lote():
    usuarios_data = request.get_json()
    try:
        resultado = usuario_dao.insertar_usuarios_lote(usuarios_data)
        if resultado:
            return jsonify({'mensaje': 'Usuarios creados correctamente', 'cantidad_insertados': len(usuarios_data)}), 201
        else:
            return jsonify({'error': 'No se pudieron insertar los usuarios'}), 400
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 400
    
@usuario_bp.route('/<id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    try:
        usuario_actualizado = Usuario(**data)
        resultado = usuario_dao.actualizar_usuario_DAO(usuario_actualizado, id_usuario)
        if resultado:
            return jsonify({'mensaje': 'Usuario actualizado correctamente'}), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@usuario_bp.route('/<id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    resultado = usuario_dao.eliminar_usuario_DAO(id_usuario)
    if resultado:
        return '', 204
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404