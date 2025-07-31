from flask import Flask, Blueprint, request, jsonify
from app.db.conexion_db import ConexionDB
from app.dao.dao_computadora import ComputadoraDAO
from app.models.model_computadora import Computadora

computadora_bp = Blueprint('computadora', __name__, '/computadoras')

conexion = ConexionDB()
pc_dao = ComputadoraDAO(conexion)

@computadora_bp.route('', methods=['GET'])
def obtener_computadoras():
    resultado = pc_dao.obtener_todas_computadora_DAO()
    return jsonify([pc.to_dict() for pc in resultado]), 200

@computadora_bp.route('/<id_computadora>', methods=['GET'])
def obtener_computadora_id(id_computadora):
    try:
        pc = pc_dao.obtener_computadora_por_id_DAO(id_computadora)
        if pc:
            return jsonify(pc.to_dict()), 200
        else:
            return jsonify({'mensaje': 'Computadora no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@computadora_bp.route('/', methods=['POST'])
def crear_pc():
    pass

@computadora_bp.route('/lote', methods=['POST'])
def crear_pc_lote():
    pass

@computadora_bp.route('/<id_computadora>', methods=['PUT'])
def actualizar_comptuadora():
    pass

@computadora_bp.route('/<id_computadora>', methods=['DELETE'])
def eliminar_computadora():
    pass