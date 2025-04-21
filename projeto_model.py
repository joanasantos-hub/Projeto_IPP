# MODEL -> Atualização das bases de dados, Implementação de funções
import json
from datetime import date, datetime, timedelta

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

# Atributos dos Pacientes
class Paciente:

    def __init__(self, nome, data_nascimento, sexo, cond_prévias, medicações, CC, NIF, contacto, NOK, NOK_contacto, localidade):
        
        self.nome = nome.strip()
        self.data_nascimento = data_nascimento.strip()
        self.sexo = sexo
        self.cond_prévias = [cond.strip() for cond in cond_prévias.split(',') if cond.strip() != '']
        self.medicações = []
        self._CC = CC
        self._NIF = NIF
        self.localidade = localidade.strip()
        self._contacto = contacto
        self.NOK = NOK.strip()
        self.NOK_contacto = NOK_contacto
        self.id = f'{self.sexo}_{self._NIF}_{self._CC}'

        if NOK == '':
            self.NOK = None
            self.NOK_contacto = None

        for med in medicações.split(','):
            
            med = med.strip()
            if med:

                blocos = med.split(':')
                if len(blocos) == 2:

                    nome_med = blocos[0].strip()
                    dosagem = blocos[1].strip()
                    self.medicações.append([nome_med,dosagem])
                else:
                    self.medicações.append()
                    
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

# Atualizar Registos de Pacientes
def guardar_registo(paciente): # O argumento recebido é o dicionário com as informações do paciente!!

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

# Processo Inicial de Log In para o Portal do Utente
def log_in(CC):

    for paciente in pacientes:
        if CC == paciente.get('_CC'):
            return True, paciente
    return False, None

# Criação do Calendário de Agendamento
def slots_calendário(data, horário_ind):

    tempo  = 30

    data_consulta = datetime.strptime(data, '%Y-%m-%d')
    if data_consulta.weekday() == 6: # Não há consultas ao domingo!!
        return False

    slots = []

    (início_dia, final_dia) = horário_ind.split('-')
    slot_0 = data_consulta.replace(hour= int(início_dia), minute= 0)
    slot_final = data_consulta.replace(hour= int(final_dia), minute= 0)

    while slot_0 < slot_final:

        next_slot = slot_0 + timedelta(minutes = tempo) # A utilização do timedelta permite definir intervalos de tempo para a duração de cada consulta!
        if not (slot_0.hour == 13 or (slot_0.hour < 13 and next_slot.hour > 14)):
            slot_almoço = f'{slot_0.strftime('%H:%M')} -  {next_slot.strftime('%H:%M')}' # HORA DE ALMOÇO DOS MÉDICOS!
            slots.append(slot_almoço)
        slot_0 = next_slot
    return slots

# Verificação de Slots Disponíveis
def slots_disponíveis(médico,data):

    slots = slots_calendário(data,médico['horas_ativas'])
    
    slots_ocupados = [consulta['horário'] for consulta in consultas if consulta['id_médico'] == médico['id'] and consulta['data'] == data]
    slots_disponíveis = [slot for slot in slots if slot not in slots_ocupados]
    
    return slots_disponíveis

# Marcação de Consultas
def marcar_consulta(nova_consulta):

    for consulta in consultas:
        if (consulta['id_médico'] == nova_consulta['id_médico'] and consulta['data'] == nova_consulta['data'] and consulta['horário'] == nova_consulta['horário']):
            return 'O horário selecionado já se encontra ocupado!'
    consultas.append(nova_consulta)

    if guardar_consulta(consultas):
        return 'Consulta marcada com sucesso!'
    else:
        return 'Erro! Não foi possível gravar a sua marcação!'
    
# Registo de Consultas Marcadas
def guardar_consulta(consulta):

    try:
        with open('consulta.json','w', encoding= 'utf-8') as f:
            json.dump(consulta, f, ensure_ascii= False,indent= 4)
        return True
    
    except:
        return f'Erro! Não foi possível gravar a sua marcação!'

# Cancelamento de Consultas Agendadas
def cancelar_cons(consulta):

    try:

        consultas.remove(consulta)
        with open('consulta.json','w', encoding= 'utf-8') as f:
            json.dump(consultas, f, ensure_ascii= False, indent= 4)
        return f'A consulta foi cancelada com sucesso!'
    
    except:
        return f'Erro! Não foi possível cancelar a sua consulta!'

# Consultas Agendadas e Não Concluídas
def consultas_futuras(paciente_id):

    cons_futuras = []
    data_atual = date.today()

    for consulta in consultas:
        if paciente_id == consulta['id_paciente']:
            
            data = datetime.strptime(consulta['data'], '%Y-%m-%d').date()
            if data >= data_atual:
                cons_futuras.append(consulta)
    
    return cons_futuras

# Histórico de Consultas do Utente
class cons_concluídas:

    def __init__(self):
        self.concluídas = []
    
    def push(self, consulta):
        self.concluídas.append(consulta)
    
    def total_concluídas(self):
        return self.concluídas

def hist_consultas(paciente_id):

    paciente_consultas = cons_concluídas()
    data_atual = date.today()

    for consulta in consultas:
        if paciente_id == consulta['id_paciente']:
            
            data = datetime.strptime(consulta['data'], '%Y-%m-%d').date()
            if data < data_atual:
                paciente_consultas.push(consulta)
    
    return paciente_consultas.total_concluídas()

def hist_medicações(paciente_id):

    for paciente in pacientes:
        if paciente_id == paciente['id']:
            return paciente['medicações']
    return []
