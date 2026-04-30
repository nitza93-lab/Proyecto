from flask import Flask, request, jsonify
from owlready2 import *

app = Flask(__name__)

# CARGAR ONTOLOGÍA
from owlready2 import *

onto = get_ontology(r"D:\Tesis\Doctorado\Proyecto\micro_ontologia\ontology-es.rdf").load()



print("Clases:", list(onto.classes()))


with onto:

    class Paciente(Thing):
        pass

    class tieneGlucosa(DataProperty):
        domain = [Paciente]
        range = [float]

    # Clases de diagnóstico
    class Hiperglucemia(Paciente):
        pass

    class Hipoglucemia(Paciente):
        pass

    class Normal(Paciente):
        pass


@app.route("/evaluar", methods=["POST"])
def evaluar():

    data = request.json
    glucosa = data.get("glucosa")

    if glucosa is None:
        return jsonify({"error": "Falta glucosa"}), 400

    glucosa = float(glucosa)

    # 🔥 CREAR PACIENTE DINÁMICO
    with onto:
        p = Paciente("paciente_temp")
        p.tieneGlucosa = [glucosa]

        # 🔥 REGLAS SIMPLES (base ontológica)
        if glucosa > 180:
            p.is_a.append(Hiperglucemia)
        elif glucosa < 70:
            p.is_a.append(Hipoglucemia)
        else:
            p.is_a.append(Normal)

    # 🔥 INFERENCIA (reasoner)
    sync_reasoner()

    # 🔥 DETECTAR CLASE
    estado = "Desconocido"

    if Hiperglucemia in p.is_a:
        estado = "Hiperglucemia"
    elif Hipoglucemia in p.is_a:
        estado = "Hipoglucemia"
    elif Normal in p.is_a:
        estado = "Normal"

    return jsonify({
        "estado": estado,
        "mensaje": "Evaluación con ontología"
    })


if __name__ == "__main__":
    app.run(port=8001, debug=True)
