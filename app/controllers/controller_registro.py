from flask import request, Blueprint, jsonify
from app.dao.dao_usuareacomp import UsuAreaCompDAO
from app.models.model_usuareacomp import UsuAreaComp
from db.conexion_db import ConexionDB
from datetime import datetime

asignacion_bp = Blueprint('usu_area_comp', __name__, url_prefix='/asignacion')
conexion = ConexionDB()
asignacion_dao = UsuAreaCompDAO(conexion)

# Función auxiliar para construir el objeto completo desde JSON
def construir_objeto_usuareacomp(data):
    return UsuAreaComp(
        id_usuario=data['id_usuario'],
        id_computadora=data['id_computadora'],
        id_area=data['id_area'],
        fecha_inicio=datetime.fromisoformat(data['fecha_inicio']),
        fecha_fin=datetime.fromisoformat(data['fecha_fin']) if data.get('fecha_fin') else None
    )


@asignacion_bp.route('/', methods=['GET'])
def obtener_asignaciones():
    try:
        asignaciones = asignacion_dao.obtener_todos_UsuAreaComp_DAO()
        resultado = [a.to_dict() for a in asignaciones]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@asignacion_bp.route('/<string:id_usuario>/<string:id_computadora>/<int:id_area>', methods=['GET'])
def obtener_asignacion(id_usuario, id_computadora, id_area):
    try:
        asignacion = asignacion_dao.obtener_UsuAreaComp_por_id_DAO(id_usuario,id_computadora,id_area)
        if asignacion:
            return jsonify(asignacion.to_dict()), 200
        else:
            return jsonify({'mensaje': 'Asignación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@asignacion_bp.route('/', methods=['POST'])
def crear_asignacion():
    datos = request.get_json()
    try:
        nueva_asignacion = construir_objeto_usuareacomp(datos)
        exito = asignacion_dao.insertar_UsuAreaComp_DAO(nueva_asignacion)
        if exito:
            return jsonify({'mensaje': 'Asignación creada con éxito'}), 201
        else:
            return jsonify({'mensaje': 'No se pudo crear la asignación'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@asignacion_bp.route('/<string:id_usuario>/<string:id_computadora>/<int:id_area>', methods=['PUT'])
def actualizar_asignacion(id_usuario, id_computadora, id_area):
    datos = request.get_json()
    try:
        asignacion_actualizacion = construir_objeto_usuareacomp(datos)
        actualizado = asignacion_dao.actualizar_UsuAreaComp_DAO(
            id_usuario, id_computadora, id_area, asignacion_actualizacion
        )
        if actualizado:
            return jsonify({'mensaje': 'Asignación actualizada'}), 200
        else:
            return jsonify({'mensaje': 'Asignación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@asignacion_bp.route('/<string:id_usuario>/<string:id_computadora>/<int:id_area>', methods=['DELETE'])
def eliminar_asignacion(id_usuario, id_computadora, id_area):
    try:
        eliminado = asignacion_dao.eliminar_UsuAreaComp_DAO(id_usuario, id_computadora, id_area)
        if eliminado:
            return jsonify({'mensaje': 'Asignación eliminada'}), 200
        else:
            return jsonify({'mensaje': 'Asignación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500