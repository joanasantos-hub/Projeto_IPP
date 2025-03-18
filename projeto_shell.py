# SHELL -> Funções principais
import json
import projeto_model as model
import projeto_view as int_gráfica

pacientes = model.bd_pac
médicos = model.bd_med
consultas = model.bd_cons
vacinação = model.bd_vac

# --------- Registo de Pacientes ---------
class Paciente:

    fnome = 'pacientes.json'

    def __init__(self, nome, idade, sexo, cond_prévias, medicações, CC, NIF, contacto, NOK, localidade):
        
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
        self.cond_prévias = cond_prévias
        self.medicações = medicações
        self.__CC = CC
        self.__NIF = NIF
        self.localidade = localidade
        self.__contacto = contacto
        self.NOK = NOK
        self.id = f'{idade}_{sexo}_{CC}'
        self.guardar_paciente()

        if medicações == '':
            self.medicações = None
    
    def to_dict(self):
        return self.__dict__
    
    def guardar_paciente(self): # TESTADA E FUNCIONA!!

        res = model.guardar_registo(self.to_dict())
        print(res)
