#from owlready2 import get_ontology, sync_reasoner
#import uuid
#
#class KnowledgeReasoner:
#    def __init__(self, owl_path):
#        self.onto = get_ontology(owl_path).load()
#
#    def evaluar_paciente(self, perfil):
#
#        with self.onto:
#
#            paciente = self.onto.Paciente(f"paciente_{uuid.uuid4()}")
#
#            paciente.tieneEdad = perfil.edad
#            paciente.tienePeso = perfil.peso
#            paciente.tieneTipoDiabetes = perfil.tipo_diabetes
#
#        # ejecutar inferencia
#        sync_reasoner()
#
#        # leer resultado REAL de la ontología
#        tratamientos = list(self.onto.tieneTratamiento[paciente])
#
#        return tratamientos



import uuid

class KnowledgeReasoner:

    def __init__(self, owl_path):
        self.owl_ok = False  # forzar fallback

    def evaluar_paciente(self, perfil):

        # 👇 usar reglas Python directamente
        tratamientos = self._reglas_python(perfil)
    
        print("DEBUG tratamientos:", tratamientos)
    
        return tratamientos



    def _reglas_python(self, perfil):

        tratamientos = []

        tipo = str(perfil.tipo_diabetes).lower().replace(" ", "")
        peso = float(perfil.peso)
        edad = int(perfil.edad)

        print("DEBUG PERFIL")
        print("TIPO DIABETES:", perfil.tipo_diabetes)
        print("PESO:", perfil.peso)
        print("EDAD:", perfil.edad)

        # =========================
        # 🧬 REGLAS TIPO 1
        # =========================
        if "tipo1" in tipo:
            tratamientos.append("Insulina basal-bolus")

            if edad > 60:
                tratamientos.append("Monitoreo frecuente")

        # =========================
        # 🧬 REGLAS TIPO 2
        # =========================
        elif "tipo2" in tipo:

            if peso > 90:
                tratamientos.append("Metformina + dieta")
                tratamientos.append("Considerar GLP-1 o SGLT2")

            else:
                tratamientos.append("Metformina")

            if edad > 60:
                tratamientos.append("Monitoreo frecuente")

            if peso > 100:
                tratamientos.append("Evaluar cirugía metabólica")

        # =========================
        # 🧬 CASO GENERAL
        # =========================
        if edad > 65:
            tratamientos.append("Control cardiovascular estricto")

        # evitar duplicados
        tratamientos = list(set(tratamientos))

        print("DEBUG PERFIL")
        print("TIPO DIABETES:", perfil.tipo_diabetes)
        print("PESO:", perfil.peso)
        print("EDAD:", perfil.edad)

        return tratamientos



