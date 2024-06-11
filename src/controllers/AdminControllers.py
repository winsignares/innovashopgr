from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from config.db import create_app
from models.EmpresaModels import Empresa, EmpresaSchema, EmpresaSchemaModulo
from models.UsuarioModels import Usuario
from models.ModuloModels import Modulos, ModuloSchema_2
from models.Empresa_ModuloModels import Empresa_Modulo
from datetime import datetime

app, db, ma = create_app()

AdminControl = Blueprint('AdminControl', __name__)

@AdminControl.route("/HomeAdmin", methods=["GET"])
def HomeEmpresa():
    return render_template('homePage.html')


@AdminControl.route("/HomeAdmin/Empresas", methods=["GET"])
def EmpresasRegistradas():
    try:
        empresas = Empresa.query.all()
        empresa_schema = EmpresaSchema(many=True)
        result = empresa_schema.dump(empresas)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@AdminControl.route("/HomeAdmin/EmpresasModulo", methods=["GET"])
def EmpresasRegistradasModulo():
    try:
        empresas = Empresa.query.all()
        empresa_schema = EmpresaSchemaModulo(many=True)
        result = empresa_schema.dump(empresas)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@AdminControl.route("/HomeAdmin/Search", methods=["GET", "POST"])
def BuscarEmpresa():
    if request.method == "GET":
        query = request.args.get('query', '').lower().strip()
        
        if query == '':
            companies = Empresa.query.all()
        else:
            companies = Empresa.query.filter(Empresa.Nombre_Empresa.ilike(f"%{query}%")).all()
        
        companies_data = []
        for company in companies:
            try:
                # Intenta convertir la fecha de string a datetime
                fecha_final = datetime.strptime(company.Fecha_Final, '%d/%m/%Y').strftime('%d/%m/%Y')
            except ValueError:
                fecha_final = company.Fecha_Final  # En caso de que la fecha no sea válida

            company_info = {
                'name': company.Nombre_Empresa,
                'time': fecha_final,  # Usar la fecha formateada
                'correo': company.Correo_Empresa,
                'nit': company.Nic_Empresa,
                'status': company.Status,
                'modules': company.Modulo
            }
            companies_data.append(company_info)

        return jsonify(companies_data)

    elif request.method == "POST":
    # Si llega un método diferente a GET o POST, puedes devolver un error 405
        return jsonify({"error": "Method not allowed"}), 405
    


@AdminControl.route("/HomeAdmin/Search2", methods=["POST"])
def BuscarEmpresaM():
    query = request.args.get('query', '').lower().strip()

    print(query)

    if query == '':
        companies = Empresa.query.all()
    else:
        companies = Empresa.query.filter(Empresa.Nombre_Empresa.ilike(f"%{query}%")).all()
    
    companies_data = []
    for company in companies:
        try:
            # Intenta convertir la fecha de string a datetime
            fecha_final = datetime.strptime(company.Fecha_Final, '%d/%m/%Y').strftime('%d/%m/%Y')
        except ValueError:
            fecha_final = company.Fecha_Final  # En caso de que la fecha no sea válida

        company_info = {
            'name': company.Nombre_Empresa,
            'time': fecha_final,  # Usar la fecha formateada
            'correo': company.Correo_Empresa,
            'nit': company.Nic_Empresa,
            'status': company.Status,
            'modules': company.Modulo
        }
        companies_data.append(company_info)

    return jsonify(companies_data)


@AdminControl.route("/HomeAdmin/AnadirEmpresa", methods=["POST", "GET"])
def AnadirEmpresa():

    fecha_actual = datetime.now()
    fecha_actual_str = fecha_actual.strftime('%Y/%m/%d')

    data = request.get_json()
    print("Datos recibidos:", data)
    Nombre = data.get('name')
    Fecha_Final = data.get('time')
    Correo = data.get('correo')
    nit = data.get('nit')
    ubicacion = data.get('ubication')
    status = data.get('status')
    modules = data.get('modules')

    new_empresa = Empresa(
        id_Empresa=None,  # SQLAlchemy manejará el autoincremento
        Nombre_Empresa=Nombre,
        Nic_Empresa=nit,
        Ubicacion_Empresa = ubicacion,
        Correo_Empresa=Correo,
        Fecha_Inicio=fecha_actual_str,
        Fecha_Final=Fecha_Final,
        Status=status,
        Modulo=modules
    )

    new_Usuario = Usuario(
        id_Usuario=None,
        Nombre_Usuario=Nombre,
        Contraseña=nit,
        CC_Usuario=nit,
        Correo_Usuario=Correo,
        Rol=2,
        Telefono = None,
        Status = status
    )
    try:
        # Añadir la nueva compañía a la sesión y guardar en la base de datos
        db.session.add(new_empresa)
        db.session.commit()

        # Añadir nuevo usuario y guardar en la base de datos
        db.session.add(new_Usuario)
        db.session.commit()

        # Si todo es exitoso, devuelve una respuesta JSON con success=True
        return jsonify({"success": True, "message": "Company created successfully."})
    except Exception as e:
        print("Error al crear la empresa:", e)
        db.session.rollback()
        return jsonify({"success": False, "message": "There was an error creating the company."})

@AdminControl.route("/HomeAdmin/Modulos") #Visualiza los modulos creados 
def ModulosRegistrados():
    try:
        ModulosEmpresa = Modulos.query.all()
        Modulo_schema = ModuloSchema_2(many=True)
        result = Modulo_schema.dump(ModulosEmpresa)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

@AdminControl.route("/HomeAdmin/AggModulos")
def AñadirModulosEmpresa():
    pass
