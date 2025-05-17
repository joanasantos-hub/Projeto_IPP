# MODEL -> Atualização das bases de dados, Implementação de funções
import json
from datetime import date, datetime, timedelta

# Carregar Bases de Dados Para a Memória -> TESTADA E FUNCIONA!
def Carregar_BD(fnome):

    try:
        with open(fnome,'r', encoding= 'utf-8') as f:
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

# Atualização do Registo de Pacientes
def guardar_registo(paciente): # O argumento recebido é o dicionário com as informações do paciente!!

    fnome = 'pacientes.json'

    for p in pacientes:
        if p.get("_CC") == paciente.get("_CC"): # Verificação de registos duplicados
            return 'Registo de paciente já existe!'
    pacientes.append(paciente) 
    
    try:
        with open(fnome,'w', encoding= 'utf-8') as f:
            json.dump(pacientes, f, ensure_ascii= False, indent= 4)
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

    tempo = 30 # Cada consulta tem uma duração base de 30 minutos
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
    
# Atualização do Registo de Consultas
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

# Histórico de Todas as Consultas do Utente (Concluídas + Futuras)
class Total_consultas:

    def __init__(self):
        self.total = []
    
    def push(self, consulta):
        self.total.append(consulta)
    
    def total_concluídas(self):
        return self.total

def hist_consultas(paciente_id):

    paciente_consultas = Total_consultas()

    for consulta in consultas:
        if paciente_id == consulta['id_paciente']:
            paciente_consultas.push(consulta)
    
    return sorted(paciente_consultas.total_concluídas(), key= lambda cons: datetime.strptime(cons['data'], '%Y-%m-%d'), reverse= True) # Organizamos as consultas pela mais recente até à mais antiga!

# Histórico de Medicações do Utente
def hist_medicações(paciente_id):

    for paciente in pacientes:
        if paciente_id == paciente['id']:
            return paciente['medicações']
    return []

def hist_certificados(paciente_id):

    for paciente in pacientes:
        if paciente_id == paciente['id'] and paciente['certificados']:
            return paciente['certificados']
    return []

# Disponibilidade de Marcação de Consultas por Especialidade em Cada Localidade
def próxima_disponibilidade(especialidade, localidade):

    tempo_máx = 8 # Número de semanas que vamos analisar para perceber se existem vagas para consultas nesse período de tempo!
    médicos_local = [med for med in médicos if med['especialidade'] == especialidade and med['localidade'] == localidade] # Médicos disponíveis por especialidade numa localidade

    atual = date.today()
    segunda_feira = atual - timedelta(days= atual.weekday()) # Início da semana atual

    for semana in range(tempo_máx):

        semana_0 = segunda_feira + timedelta(weeks= semana)
        semana_fim = semana_0 + timedelta(days= 5) # As semanas foram anteriormente definidas de segunda a sábado!
    
        for dias in range(6):
            dia = (semana_0 + timedelta(days= dias)).strftime('%Y-%m-%d')

            for médico in médicos_local:
                if slots_disponíveis(médico,dia):
                    return f'Semana {semana_0.day}/{semana_0.month} - {semana_fim.day}/{semana_fim.month}'
    
    return f'Sem disponibilidade nas próximas {tempo_máx} semanas'

def disponibilidade_local(localidade):

    especialidades = {med['especialidade'] for med in médicos if med['localidade'] == localidade} # Set de modo a termos uma lista das especialidades SEM repetições
    disponibilidade = []

    for esp in especialidades:
        semana = próxima_disponibilidade(esp, localidade)
        disponibilidade.append([esp, semana])
    return disponibilidade

# Atributos dos Registados na Campanha de Vacinação
class Vacinação:

    def __init__(self, nome, data_nascimento, sexo, certificados, vacina, dose, CC, contacto, localidade):
        
        self.nome = nome.strip()
        self.data_nascimento = data_nascimento.strip()
        self.sexo = sexo
        self.certificados = []
        self.vacina = vacina
        self.dose = dose
        self._CC = CC
        self.localidade = localidade.strip()
        self._contacto = contacto

        for certif in certificados.split(','):
            
            certif = certif.strip()

            if certif:
                blocos = certif.split(':')

                if len(blocos) == 3:
                    vac = blocos[0].strip()
                    d = blocos[1].strip()
                    data_adm = blocos[2].strip()
                    self.certificados.append([vac,d,data_adm])
                
                else:
                    self.certificados.append()
                    
    def idade(self): # Atualização automática da idade da pessoa registada para vacinação

        nascimento = datetime.strptime(self.data_nascimento, '%Y-%m-%d')
        atual = datetime.today()
        idade = atual.year - nascimento.year - ((atual.month, atual.day) < (nascimento.month, nascimento.day))
        return idade

    def to_dict(self):

        info_vacinação = self.__dict__.copy() # Criamos uma cópia do dicionário de modo a não perder as informações originais quando for realizada a alteração da chave 'idade'
        info_vacinação['idade'] = self.idade()
        return info_vacinação
    
# Atualização do Registo de Inscrições para Vacinação
def guardar_vacinação(inscrição): # O argumento recebido é o dicionário com as informações da inscrição!!

    fnome = 'camp_vac.json'

    for i in campanha:
        if i.get('_CC') == inscrição.get('_CC') and i.get('dose') == inscrição.get('dose') and i.get('vacina') == inscrição.get('vacina'): # Verificação de registos duplicados
            return 'A inscrição já foi realizada!'
    campanha.append(inscrição) 
    
    atualizar_certif = False

    if inscrição['certificados']:
        for p in pacientes:
            if inscrição['_CC'] == p['_CC']:
                p['certificados'] = inscrição['certificados']
                atualizar_certif = True

    if atualizar_certif:
        try:
            with open('pacientes.json', 'w', encoding= 'utf-8') as f2:
                json.dump(pacientes, f2, ensure_ascii= False, indent= 4)

        except Exception as e: print(e)

    try:
        with open(fnome,'w', encoding= 'utf-8') as f:
            json.dump(campanha, f, ensure_ascii= False, indent= 4)
        return f'Inscrição registada com sucesso!'

    except:
        return f'Erro! Não foi possível guardar a inscrição!'

# Campanha de Vacinação -> Distribuição Faixa Etária
def dist_faixas_etárias():
    
    res = {'0-17': 0, '18-30': 0, '31-50': 0, '51-60': 0, '61-70': 0, '>70': 0 }

    for i in campanha:
        idade = i['idade']

        if idade <= 17:
            res['0-17'] = res['0-17'] + 1

        elif idade in range(18,31):
            res['18-30'] = res['18-30'] + 1

        elif idade in range(31,51):
            res['31-50'] = res['31-50'] + 1

        elif idade in range(51,61):
            res['51-60'] = res['51-60'] + 1

        elif idade in range(61,71):
            res['61-70'] = res['61-70'] + 1
        
        elif idade > 70:
            res['>70'] = res['>70'] + 1
    return res

# Campanha de Vacinação -> Distribuição Sexo
def dist_sexo():

    res = {'F': 0, 'M': 0}

    for i in campanha:
        sexo = i['sexo']

        if sexo in res:
            res[sexo] = res[sexo] + 1
    return res

# Campanha de Vacinação -> Distribuição Localidade
def dist_localidade():

    res = {'Sobradelo da Goma': 0, 'Aldeia das Dez': 0, 'Janeiro de Cima': 0, 'Aveleda e Rio de Onor': 0, 'Barrancos': 0, 'Piódão': 0,
           'Monte da Pedra': 0, 'Cachopo': 0, 'Alferce': 0, 'Castro Laboreiro': 0, 'S. Martinho das Amoreiras': 0, 'Martim Longo': 0}
    
    for i in campanha:
        localidade = i['localidade']

        if localidade in res:
            res[localidade] = res[localidade] + 1
    return res

# Campanha de Vacinação -> Distribuição Tipo de Vacina
def dist_vacina():

    res = {'COVID-19': 0, 'Gripe A': 0, 'HPV': 0, 'Tétano e Difteria': 0}

    for i in campanha:
        vacina = i['vacina']

        if vacina in res:
            res[vacina] = res[vacina] + 1
    return res
