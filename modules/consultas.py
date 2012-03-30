#!/usr/bin/env python
# coding: utf8
import sqlite3
import os

def conecta_bd(ruta):
    cnn = sqlite3.connect(os.path.join(ruta,'databases/storage.sqlite'))
    cursor = cnn.cursor()
    return cursor

def busca_proveedor(id, ruta):
    cursor = conecta_bd(ruta)
    prv = (id,)
    cursor.execute('select nombre from proveedores where id=?',prv)
    nombre = cursor.fetchone()
    return nombre[0]

def busca_producto(id, ruta):
    cursor = conecta_bd(ruta)
    prv = (id,)
    cursor.execute('select * from productos where id=?',prv)
    producto = cursor.fetchone()
    return producto
    
def selecciona_productos(proveedor, nombre, ruta):
    cursor = conecta_bd(ruta)
    criterio = (proveedor, nombre,)
    sql = """
    select * from productos
    where proveedor_id = ?
    and nombre like ?
    """
    cursor.execute(sql,criterio)
    productos = cursor.fetchall()
    return productos
