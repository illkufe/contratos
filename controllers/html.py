# coding: utf8
# try something like

from consultas import selecciona_productos
from consultas import busca_producto


def index():
    contratos = db(db.contratos.id>0).select()
    return dict(contratos = contratos)

def contrato():
    este_contrato = db.contratos(request.args(0)) or redirect(URL('html','index'))
    if request.args(2)=='DEL':
        db(db.det_contratos.id==int(request.args(1))).delete()
        db.commit()
        redirect(URL('html','contrato', args=request.args(0)))        
    productos = db(db.det_contratos.contrato_id==este_contrato.id).select()        
    return dict(contrato=este_contrato,productos=productos)

def modproductos():
    este_detalle = db.det_contratos(request.args(0)) or redirect(URL('html','index'))
    if request.env.request_method == "POST":
        c = int(request.post_vars.pro_cantidad)
        p = float(request.post_vars.pro_precio)
        n = c * p
        este_detalle.update_record(precio_lista=p, cantidad=c, neto=n)
    return dict(detalle=este_detalle)

def buscaproductos():
    este_contrato = db.contratos(request.args(0)) or redirect(URL('html','index'))
    productos = []
    if request.env.request_method == "POST":
        if request.vars.aceptar == 'Buscar':
            if request.vars.descripcion: 
                datos = 'en busqueda'
                descripcion = '%' + request.vars.descripcion + '%'
                productos = selecciona_productos(este_contrato.proveedor,descripcion,request.folder)
        elif request.vars.aceptar == 'Aceptar':
            nump = 0
            datos = eval(str(request.vars.productos))
            if 1 == 1:
                for producto in datos:
                    nump = nump + 1
                    p = busca_producto(int(producto), request.folder)
                    db.det_contratos.insert(contrato_id=este_contrato.id,cod_producto=p[0],precio_lista=p[3],cantidad=0,neto=0)
                    db.commit()
            else:
                    nump = nump + 1
                    p = busca_producto(int(datos), request.folder)
                    db.det_contratos.insert(contrato_id=este_contrato.id,cod_producto=p[0],precio_lista=p[3],cantidad=0,neto=0)
                    db.commit()
            
            request.vars.productos=[]
            msj = 'Se grabaron %s en contrato n° %s' %(str(nump),str(este_contrato.id)) 
            
            response.flash = msj
    return dict(productos=productos, contrato=este_contrato)
