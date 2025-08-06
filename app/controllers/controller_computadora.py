from flask import Blueprint, request, jsonify
from db.conexion_db import ConexionDB
from app.dao.dao_computadora import ComputadoraDAO
from app.models.model_computadora import Computadora

computadora_bp = Blueprint('computadora', __name__, url_prefix='/computadoras')

conexion = ConexionDB()
pc_dao = ComputadoraDAO(conexion)

@computadora_bp.route('/', methods=['GET'])
def obtener_computadoras():
    resultado = pc_dao.obtener_todas_computadora_DAO()
    if resultado:
        return jsonify([pc.to_dict() for pc in resultado]), 200
    if resultado is None:
        return jsonify({'mensaje': 'No hay datos de la tabla computadora'}), 204
    else:
        return jsonify({'error': 'Error al mostrar todos los datos'}), 400

@computadora_bp.route('/<id_computadora>', methods=['GET'])
def obtener_computadora_id(id_computadora):
    try:
        pc = pc_dao.obtener_computadora_por_id_DAO(id_computadora)
        if pc:
            return jsonify(pc.to_dict()), 200
        else:
            return jsonify({'mensaje': 'Computadora no encontrada'}), 404
    except Exception as e:
        return jsonify({'Error': str(e)}), 400

@computadora_bp.route('/', methods=['POST'])
def crear_pc():
    datos = request.get_json()
    try:
        pc = Computadora(**datos)
        resultado = pc_dao.insertar_computadora_DAO(pc)
        if resultado:
            return jsonify({'mensaje': f'Computadora {pc.id_computadora} creado e insertado correctamente'}), 201
        else:
            return jsonify({'mensaje': 'Error al insertar la computadora'}), 400
    except Exception as e:
        return jsonify({'Error': str(e)}), 400

@computadora_bp.route('/lote', methods=['POST'])
def crear_pc_lote():
    datos = request.get_json()
    try:
        pc = [Computadora(**fila) for fila in datos]
        resultado = pc_dao.insertar_computadoras_lote(pc)
        if resultado:
            return jsonify({'mensaje': f'{len(pc)} creado e insertados correctamente'}), 201
        else:
            return jsonify({'error': 'Error al insertar el lote de computadoras'}), 400
    except Exception as e:
        return jsonify({'Error': str(e)}), 400
    

@computadora_bp.route('/<id_computadora>', methods=['PUT'])
def actualizar_comptuadora(id_computadora):
    datos = request.get_json()
    try:
        pc = Computadora(**datos)
        resultado = pc_dao.actualizar_computadora_DAO(pc, id_computadora)
        if resultado:
            return '', 204
        else:
            return jsonify({'error': 'Error al actualizar la computadora'}), 400
    except Exception as e:
        return jsonify({'Error': str(e)})

@computadora_bp.route('/<id_computadora>', methods=['DELETE'])
def eliminar_computadora(id_computadora):
    resultado = pc_dao.eliminar_computadora_DAO(id_computadora)
    if resultado:
        return jsonify({'mensaje': f'{id_computadora} eliminado correctamente'}), 204
    else:
        return jsonify({'error': 'Error al eliminar la computadora'}), 404
    
@computadora_bp.route('/validar/<id_computadora>', methods=['GET'])
def existe_computadora(id_computadora):
    try:
        resultado = pc_dao.existe_computadora_DAO(id_computadora)
        if resultado:
            return jsonify({'mensaje': f'La computadora {id_computadora} existe'}), 204
        else:
            return jsonify({'error': f'La computadora {id_computadora} no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 404