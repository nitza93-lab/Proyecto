from owlready2 import *

class DiabetesReasoner:
    def __init__(self, path_owl):
        self.onto = get_ontology(path_owl).load()

    def evaluar_paciente(self, perfil):
        with self.onto:
            paciente = self.onto.Paciente("temp_paciente")

            paciente.tieneEdad = perfil.edad
            paciente.tienePeso = perfil.peso
            paciente.tieneTipoDiabetes = perfil.tipo_diabetes

        sync_reasoner()

        return list(paciente.requiereTratamiento)
