# MODEL -> Atualização das bases de dados, Implementação de funções
import json
#import projeto_shell as logic
#import projeto_view as int_gráfica

# Carregar Bases de Dados Para a Memória -> ARRANQUE DO SISTEMA
def Carregar_Pacientes(fnome):

    try:
        with open(fnome,'r', encoding='utf-8') as f:
            pacientes = json.load(f)
        return pacientes
    
    except (FileNotFoundError, json.JSONDecodeError):
        return f'Erro! Ficheiro vazio ou não encontrado!'

def Carregar_Médicos(fnome):

    try:
        with open(fnome,'r', encoding='utf-8') as f:
            médicos = json.load(f)
        return médicos
    
    except (FileNotFoundError, json.JSONDecodeError):
        return f'Erro! Ficheiro vazio ou não encontrado!'

def Carregar_Consultas(fnome):

    try:
        with open(fnome,'r', encoding='utf-8') as f:
            consultas = json.load(f)
        return consultas
    
    except (FileNotFoundError, json.JSONDecodeError):
        return f'Erro! Ficheiro vazio ou não encontrado!'
    
def Carregar_Campanha(fnome):

    try:
        with open(fnome,'r', encoding='utf-8') as f:
            campanha = json.load(f)
        return campanha
    
    except (FileNotFoundError, json.JSONDecodeError):
        return f'Erro! Ficheiro vazio ou não encontrado!'

bd_pac = Carregar_Pacientes('pacientes.json')
bd_med = Carregar_Médicos('médicos.json')
bd_cons = Carregar_Consultas('consulta.json')
bd_vac = Carregar_Campanha('camp_vac.json')

# Atualizar Registos de Clientes -> TESTADA E FUNCIONA!!
def guardar_registo(paciente): # O argumento recebido é o dicionário criado no SHELL!!

    fnome = 'pacientes.json'

    for p in bd_pac:
        if p.get("_CC") == paciente.get("_CC"): # Verificação de registos duplos -> Se já existir o registo, este não será adicionado à BD
            print("Registro duplicado encontrado para CC:", paciente.get("_CC"))
            return 'Registo de paciente já existe!'
    bd_pac.append(paciente) # Atualização da base de dados
    
    try:
        with open(fnome,'w',encoding='utf-8') as f: # Reposição do conteúdo da base de dados
            json.dump(bd_pac,f,ensure_ascii=False, indent=4)
        return f'Paciente registado com sucesso!'

    except:
        return f'Erro! Não foi possível guardar o registo!'
    
def log_in(CC):

    for paciente in bd_pac:
        if CC == paciente.get('_CC'):
            return True
    print('Registo de utente não encontrado! Por favor realize a sua inscrição na plataforma')
    return False
