# MODEL -> Atualização da base de dados, Implementação de funções
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
