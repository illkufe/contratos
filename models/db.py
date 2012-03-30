# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite')

db.define_table('contratos',
    Field('proveedor', 'integer'),
    Field('cliente', 'string',length=50))

db.define_table('det_contratos',
    Field('contrato_id', db.contratos),
    Field('cod_producto', 'integer'),
    Field('precio_lista', 'double'),
    Field('cantidad', 'integer'),
    Field('neto', 'double'))

existe_contratos = db(db.contratos.id > 0).select().first()
if not existe_contratos:
    from gluon.contrib.populate import populate
    populate(db.contratos,15)
    populate(db.det_contratos, 75)

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
