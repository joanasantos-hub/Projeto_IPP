# MODEL -> Atualização das bases de dados, Implementação de funções
import json
from datetime import datetime

# Carregar Bases de Dados Para a Memória -> TESTADA E FUNCIONA!
def Carregar_BD(fnome):

    try:
        with open(fnome,'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados
    
    except (FileNotFoundError, json.JSONDecodeError):
        return f'Erro! Ficheiro vazio ou não encontrado!'

pacientes = Carregar_BD('pacientes.json')
médicos = Carregar_BD('médicos.json')
consultas = Carregar_BD('consulta.json')
campanha = Carregar_BD('camp_vac.json')

# Atribuitos dos Pacientes
class Paciente:

    def __init__(self, nome, data_nascimento, sexo, cond_prévias, medicações, CC, NIF, contacto, NOK, NOK_contacto, localidade):
        
        self.nome = nome.strip()
        self.data_nascimento = data_nascimento.strip()
        self.sexo = sexo
        self.cond_prévias = [cond.strip() for cond in cond_prévias.split(',') if cond.strip() != '']
        self.medicações = [meds.strip() for meds in medicações.split(',')if meds.strip() != '']
        self._CC = CC
        self._NIF = NIF
        self.localidade = localidade.strip()
        self._contacto = contacto
        self.NOK = NOK.strip()
        self.NOK_contacto = NOK_contacto
        self.certificados = []
        self.consultas = []
        self.id = f'{self.sexo}_{self._NIF}_{self._CC}'

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

# Atributos dos Médicos
class Médico:

    def __init__(self, id, especialidade, horas_ativas, localidade, contacto):
        
        self.id = id
        self.especialidade = especialidade
        self.horas_ativas = horas_ativas
        self.localidade = localidade
        self.contacto = contacto

        for med in médicos:

            id = med['id']
            especialidade = med['especialidade']
            horas_ativas = med['horas_ativas']
            localidade = med['localidade']
            contacto = med['contacto']
    
    def consulta(self, horas_ativas):

        dias_semana = 7
        horas = horas_ativas.split('-')
        slots = (int(horas[1]) - int(horas[0])) * 3

        consultas = [[0 for d in range(dias_semana)] for s in range(slots)]

    def tabela_consultas(self, consultas):

        for linha in consultas:
            for elem in linha:
                print(elem, end=' ')
            print()

# Atualizar Registos de Pacientes -> TESTADA E FUNCIONA!!
def guardar_registo(paciente): # O argumento recebido é o dicionário criado no CONTROLLER!!

    fnome = 'pacientes.json'

    for p in pacientes:
        if p.get("_CC") == paciente.get("_CC"): # Verificação de registos duplicados
            return 'Registo de paciente já existe!'
    pacientes.append(paciente) 
    
    try:
        with open(fnome,'w',encoding='utf-8') as f:
            json.dump(pacientes,f,ensure_ascii=False, indent=4)
        return f'Paciente registado com sucesso!'

    except:
        return f'Erro! Não foi possível guardar o registo!'

# Processo Inicial de Log In para o Portal do Utente -> TESTADA E FUNCIONA!!   
def log_in(CC):

    for paciente in pacientes:
        if CC == paciente.get('_CC'):
            return True
    return False