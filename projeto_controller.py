# CONTROLLER -> Arranque da Interface, Passagem de Informação (Model -> View)
import projeto_model as model
import projeto_view as view
from datetime import datetime, timedelta

# Processamento do Novo Registo de Utente
def processar_registo(values):

    try:
        paciente = model.Paciente(
            nome = values['-NOME-'],
            data_nascimento = values['-DOB-'],
            sexo = values['-SEXO-'],
            cond_prévias = values['-COND-'],
            medicações = values['-MEDS-'],
            CC = int(values['-CC-']) if values['-CC-'] else None,
            NIF = int(values['-NIF-']) if values['-NIF-'] else None,
            contacto = int(values['-CP-']) if values['-CP-'] else None,
            NOK = values['-NOK-'],
            NOK_contacto = int(values['-CNOK-']) if values['-CNOK-'] else None,
            localidade = values['-LOCAL-']
        )
    
        res = model.guardar_registo(paciente.to_dict())
        return res

    except Exception as e:
        print(e)

# Processamento do Log In do Utente
paciente_logged = None

def check_login(values):

    try:
        sucesso, paciente = model.log_in(CC = int(values['-UTENTE_CC-']))

        if sucesso:
            global paciente_logged
            paciente_logged = paciente
            return True
        
        else:
            return False
        
    except Exception as e:
        print(e)

def info_paciente_logged(): # Informações do paciente que realizou log in no portal!
    return paciente_logged

# Seleção de Médicos por Especialidade
def médicos_especialidade(especialidade):
    return [med for med in model.médicos if med['especialidade'] == especialidade]

# Criação do Calendário por Especialidade
def agenda_especialidade(especialidade, semana_0):

    med_especialistas = médicos_especialidade(especialidade)

    if not med_especialistas:
        return None, None, None
    
    semana = [semana_0 + timedelta(days = i) for i in range(6)]
    data_início = semana[0].strftime('%Y-%m-%d')
    med = med_especialistas[0] # Todos os médicos de cada especialidade possuem o mesmo horário!

    slots = model.slots_calendário(data_início, med['horas_ativas'])

    agenda = {}
    consultas = model.consultas

    for dia_index, dia in enumerate(semana):

        data = dia.strftime('%Y-%m-%d')

        for slot in slots:

            # Slots são definidos para cada médico! Se um médico tiver um slot ocupado continua a ser possível agendar esse slot para outros médicos especialistas!
            slot_ocupado = [consulta['id_médico'] for consulta in consultas if (consulta['data'] == data and consulta['horário'] == slot and consulta['especialidade'] == especialidade)]
            
            med_restantes = [med for med in med_especialistas if med['id'] not in slot_ocupado] # Criamos uma lista dos médicos que ainda possuem vagas para o slot selecionado!

            if med_restantes:
                restantes_id = tuple(med['id'] for med in med_restantes)
                display = 'Disponível'
                agenda[(dia_index,slot)] = {'médico': display, 'marcada': False, 'id_médico': restantes_id}

            else:
                slot_ocupado_id = slot_ocupado[0]
                display = 'Ocupado'
                agenda[(dia_index,slot)] = {'médico': display, 'marcada': True, 'id_médico': slot_ocupado_id}
    
    return semana, slots, agenda

# Processamento da Marcação de Consultas
def processar_marcar_consulta(data, slot, especialidade, med_id, paciente_id):

    for med in model.médicos:
        if med['id'] == med_id:
            med_contacto = med['contacto']

    nova_consulta = {
        
        "data": data, 
        "horário": slot, 
        "especialidade": especialidade.upper(), 
        "id_médico": med_id, 
        "id_paciente": paciente_id,
        "contacto_médico": med_contacto
    }
    
    res = model.marcar_consulta(nova_consulta)
    return res

# Processamento da Informação de Todas as Consultas do Paciente (Concluídas + Futuras)
def info_hist_consultas(paciente_id):
    
    consultas_ind = model.hist_consultas(paciente_id)
    return consultas_ind

# Processamento da Informação de Prescrições Médicas do Paciente
def info_hist_medicações(paciente_id):
    
    medicações_ind = model.hist_medicações(paciente_id)
    return medicações_ind

# Processamento da Informação de Certificados de Vacinação do Paciente
def info_hist_certificados(paciente_id):
    
    certificados_ind = model.hist_certificados(paciente_id)
    return certificados_ind

# Processamento da Informação de Consultas Não Concluídas do Paciente
def info_consultas_futuras(paciente_id):

    consultas_fut = model.consultas_futuras(paciente_id)
    return consultas_fut

# Processamento da Informaçõa de Consultas A Cancelar
def processar_cancelar_consulta(consulta):

    res = model.cancelar_cons(consulta)
    return res

# Informações Médicos Especialistas
def get_info_médicos():

    res = model.médicos
    return res

# Processamento da Informação de Disponibilidade de Marcação de Consultas Por Localidade
def info_disponibilidade_local(localidade):

    res = model.disponibilidade_local(localidade)
    return res

# Processamento do Novo Registo para Vacinação
def processar_vacinação(values):

    try:
        vacinação = model.Vacinação(
            nome = values['-NOME-'],
            data_nascimento = values['-DOB-'],
            sexo = values['-SEXO-'],
            certificados = values['-CERTIF-'],
            vacina = values['-VACINA-'],
            dose = values['-DOSE-'],
            CC = int(values['-CC-']) if values['-CC-'] else None,
            contacto = int(values['-CP-']) if values['-CP-'] else None,
            localidade = values['-LOCAL-']
        )
    
        res = model.guardar_vacinação(vacinação.to_dict())
        return res

    except Exception as e:
        print(e)

# Processamento das Informações das Distruibuições de Inscrições na Campanha de Vacinação
def info_dist_faixa():

    res = model.dist_faixas_etárias()
    return res

def info_dist_sexo():

    res = model.dist_sexo()
    return res

def info_dist_localidade():

    res = model.dist_localidade()
    return res

def info_dist_vacina():

    res = model.dist_vacina()
    return res

def main():
    view.run_interface()

if __name__ == "__main__":
    main()
