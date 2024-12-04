# Jsonify siempre para resultados finales y Request siempre
import json
from flask import Flask, jsonify, request


app = Flask(__name__)

# Base de datos simulada
humans = [
    {
        "id" : 1,
        "name" : "hugo",
        "last_name" : "pinto"
    },
    {
        "id" : 2,
        "name" : "deimian",
        "last_name" : "montrow"
    },
    {
        "id" : 3,
        "name" : "elio",
        "last_name" : "colmenares"
    }

]
    



@app.route('/health-check')
def health_check():
    return "ok"


# 1- Los try-except sera muy importantes para manejar solicitudes de usuarios
# 2- Ahora en vez de acceder a la base datos directamente o usar for , usaremos ID + Filter 
@app.route('/person', methods=['GET'])
def get_all_human():
    try:
        return jsonify(humans), 200
    except Exception as error:
        # En Error incluso puedo acceder una propiedad (?
        # print(error.args)
        return {"Mensaje": "Ha ocurrido un error en el servidor"}, 500
    

# Si el usuario escribe un algo incorrecto en la URL de mi endpoint (Fijate lo que pide el endpoint <:>)
# En ese caso me tira un 404 y NO se ejecuta el def de mi endpoint, asi que except no sirve en ese caso
# Para eso controlamos ese 404 fuera de mi endpoint con Este decorador
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": "La URL no es válida o el recurso no fue encontrado"}), 404


@app.route('/person/<int:theid>', methods=['GET'])
def get_person(theid):
    try:
        # Asegurarnos de que 'result' sea una lista
        result = list(filter(lambda unit: unit["id"] == theid, humans))
        print(f"Resultado del filtro: {result}")
        
        # Si encontramos resultados, los retornamos, si no, retornamos un mensaje de no encontrado
        if result:
            return jsonify(result), 201
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as error:
        print(f"Error: {error}")
        return {"message": "No se pudo consultar la url", "error": str(error)}, 500
        

# Ya, es hora de agregar un POST!
@app.route('/person', methods=['POST'])
def add_new_human():
    # Como manejamos el request del usuario (json, get_json, Etc)
    body = request.json
    try:
        
        # METODO 1
        # Ahora "obligamos" al usuario a que escriba correctamente las keys en el diccionario del Post
        # Esto significa si la key "name" no existe...
        # if body.get("name") is None:
        #     return {"message" : 'Se necesita una key "Name"'}
        # if body.get("last_name") is None:
        #     return {"message" : 'Se necesita una key "Lastname"'}
    
        # METODO 2 (Teoria de conjuntos)

        required_fields = {"name", "last_name"}
        missing_fields = required_fields - set(body.keys())
        if missing_fields:
            # No olvides join para "limpiar" codigos con mucho contenido
            return jsonify({"message": f"missing required fields: {", ".join(required_fields)}"}), 201


        # OJO hay mas de una forma de manejar esta logica
        # hidden: Igualar si ambos objetos son iguales
        body.update({"id" : len(humans) + 1})
        humans.append(body)
        return {"Message" : "Éxito! Se agrego el nuevo usuario correctamente"}
    except Exception as error: 
        return jsonify({"message" : f"Se intento ejecutar el post, pero falló...{error}"}), 500



# Ahora si queremos actualizar un user (Similar al Post )
@app.route('/person/<int:theid>', methods=['PUT'])
def update_human(theid):
    body = request.json
    try:
        if body.get("name") is None:
                return {"message" : 'Se necesita una key "Name"'}
        if body.get("last_name") is None:
                return {"message" : 'Se necesita una key "Lastname"'}
        
        if theid > len(humans):
            return {"message" : "Numero de ID incorrecto!"}, 400
        
        # No olvides que este lambda te esta devolviendo lo mismo que esta iterando (no solo ["id"]) 
        # y mientras pase por la condicion, si no se ignora y pasa al sgte
        new_human = list(filter(lambda unit : unit["id"] == theid, humans))
        print('Este es el valor de mi lambda new human: ', new_human)
        
        if new_human:
            new_human = new_human[0]
            new_human["name"] = body["name"]
            new_human["last_name"] = body["last_name"]

        return jsonify(new_human), 200
    except Exception as error:
        print("Se intentó hacerle el put pero falló", str(error))

# Y por ultimooo Deletear !
@app.route('/person/<int:theid>', methods=['DELETE'])
def simple_delete(theid):
    try:
        result = list(filter(lambda unit : unit["id"] == theid, humans))
        if result:
            new_human = list(filter(lambda unit : unit["id"] != theid, humans))
            # !Importante usar [:] ya que no puedo modificar directamente una variable global
            # dentro una funcion
            humans[:] = new_human
            return jsonify({}), 204.
    except Exception as error:
        return jsonify({"Message" : "User not found"}),404



# Escto me recuerda al ultimo codigo del Tkinter que solo servia para ejecutarlo
# y lo dejaba al final ekisde        
if __name__ == '__main__': 
    app.run(host='0.0.0.0',debug=True)





