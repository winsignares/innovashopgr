from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from config.db import create_app
from models.UsuarioModels import Usuario
from models.VendedorModels import Vendedor, VendedorSchema

app, db, ma = create_app()

EmpresaContro = Blueprint('EmpresaContro', __name__)


@EmpresaContro.route("/HomeEmpresa/Vendedor", methods=["GET"])
def VendedorRegistradas():
    try:
        empresas = Vendedor.query.all()
        Vendedor_schema = VendedorSchema(many=True)
        result = Vendedor_schema.dump(empresas)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@EmpresaContro.route("/HomeEmpresa/AnadirVendedor", methods=["POST", "GET"])
def AnadirVendedor():
    data = request.json
    name = data['nameEmployee']
    last_name = data['lastNameEmployee']
    time = data['timeEmployee']
    correo = data['correoEmployee']
    cc = data['ccEmployee']
    status = data['statusEmployee']
    salary = data['salaryEmployee']

    new_Usuario = Usuario(
        id_Usuario=None,
        Nombre_Usuario=name,
        Apellido_Usuario=last_name,
        Contraseña=cc,
        CC_Usuario=cc,
        Correo_Usuario=correo,
        Rol = 3,  # Empleado
        Telefono=None,
        Status = status
        )
    
    db.session.add(new_Usuario)
    db.session.commit()

    
    try:
        usuario = Usuario.query.filter_by(CC_Usuario = cc).first()

        if usuario:
            return jsonify({'success': True, 'id_Usuario': usuario.id_Usuario})


        new_employee = Vendedor(
            id_Vendedor = None,
            id_Usuario = 'id_usuario',
            Fecha_Inicio = time,
            Fecha_Fin = time,
            Status=status,
            Salario=salary,
            id_Empresa = 14
        )

        db.session.add(new_employee)
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

