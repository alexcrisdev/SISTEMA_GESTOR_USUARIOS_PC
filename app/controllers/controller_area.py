from flask import request, Blueprint, jsonify
from app.models.model_area import Area
from app.dao.dao_area import AreaDAO
from app.db.conexion_db import ConexionDB

area_bp = Blueprint('area', __name__, url_prefix='/areas')

conexion = ConexionDB()
area_dao = AreaDAO(conexion)

@area_bp.route('', methods=['GET'])
def obtener_areas():
    resultados = area_dao.obtener_todos_area_DAO()
    return jsonify([u.to_dict() for u in resultados]), 200

@area_bp.route('/<int:id_area>', methods=['GET'])
def obtener_area_por_id(id_area):
    area = area_dao.obtener_area_por_id_DAO(id_area)
    if area:
        return jsonify(area.to_dict()), 200
    return jsonify({'mensaje': 'Area con encontrado'}), 404

@area_bp.route('', methods=['POST'])
def crear_area():
    datos = request.get_json()
    try:
        area = Area(**datos)
        resultado = area_dao.insertar_area_DAO(area)
        if resultado:
            return jsonify({'mensaje': 'Area creada correctamente'}), 201
        else:
            return jsonify({'error': 'No se pudo insertar el área'}), 400
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 400
    
@area_bp.route('/lote', methods=['POST'])
def crear_areas_lotes():
    datos = request.get_json()
    try:
        lista_objetos_area = [Area(nombre_area=d["nombre_area"]) for d in datos]
        areas = area_dao.insertar_area_lotes_DAO(lista_objetos_area)
        if areas:
            return jsonify({'mensaje': f"{len(datos)} creadas correctamente"}), 201
        else: 
            return jsonify({'error': 'Error al crear e insertar las áreas'}), 400
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 400
    
@area_bp.route('/<int:id_area>', methods=['PUT'])
def actualizar_area(id_area):
    datos = request.get_json()
    try:
        area_nueva = AreaDAO(**datos)
        resultado = area_dao.actualizar_area_DAO(area_nueva, id_area)
        if resultado:
            return jsonify({'mensaje': 'Área actualizada correctamente'}), 200
        else:
            return jsonify({'error': 'No se pudo actualizar el área'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@area_bp.route('/<int:id_area>', methods=['DELETE'])
def eliminar_area(id_area):
    resultado = area_dao.eliminar_area_DAO(id_area)
    if resultado:
        return '', 204
    else:
        return jsonify({'error': 'Área no encontrada'}), 404