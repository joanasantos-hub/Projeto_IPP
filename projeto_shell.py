# SHELL -> Funções principais
import json
import projeto_model as model
import projeto_view as int_gráfica
from datetime import datetime

pacientes = model.bd_pac
médicos = model.bd_med
consultas = model.bd_cons
vacinação = model.bd_vac

# Registo de Pacientes ---------
class Paciente:

    fnome = 'pacientes.json'

    def __init__(self, nome, data_nascimento, sexo, cond_prévias, medicações, CC, NIF, contacto, NOK, NOK_contacto, localidade):
        
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.cond_prévias = [cond.strip() for cond in cond_prévias.split(',') if cond.strip() != '']
        self.medicações = [med.strip() for med in medicações.split(',')if med.strip() != '']
        self.__CC = CC
        self.__NIF = NIF
        self.localidade = localidade
        self.__contacto = contacto
        self.NOK = NOK
        self.NOK_contacto = NOK_contacto
        self.id = f'{sexo}_{NIF}_{CC}'
        self.guardar_paciente()

        if NOK == '':
            self.NOK = None
            self.NOK_contacto = None
    
    def idade_paciente(self): # Atualização automática da idade do paciente

        nascimento = datetime.strptime(self.data_nascimento, '%Y-%m-%d')
        atual = datetime.today()
        idade = atual.year - nascimento.year - ((atual.month, atual.day) < (nascimento.month, nascimento.day))
        return idade

    def to_dict(self):

        info_paciente = self.__dict__.copy() # Criamos uma cópia do dicionário de modo a não perder as informações originais quando for realizada a alteração da chave 'idade'
        info_paciente['idade'] = self.idade_paciente()
        return info_paciente
    
    def guardar_paciente(self): # TESTADA E FUNCIONA!!

        res = model.guardar_registo(self.to_dict())
        print(res)
