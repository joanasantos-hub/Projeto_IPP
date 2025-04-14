# CONTROLLER -> Controlo do Sistema, Funções de Arranque
import json
import projeto_model as model
import projeto_view as view
from datetime import datetime, timedelta
import random

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
    
    except:
        pass

paciente_logged = None # Variável global que irá armazenar as informações do paciente que realizou log in!

def check_login(values):

    try:
        sucesso, paciente = model.log_in(CC = int(values['-UTENTE_CC-']))

        if sucesso:

            global paciente_logged
            paciente_logged = paciente
            return True
        else:
            return False
        
    except:
        pass

def info_paciente_logged(): # Retornamos as informações do paciente para que possam ser acedidas no portal!
    return paciente_logged

# Seleção de Médicos por Especialidade
def médicos_especialidade(especialidade):
    return [med for med in model.médicos if med['especialidade'] == especialidade]

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

    for dia_index,dia in enumerate(semana):

        data = dia.strftime('%Y-%m-%d')

        for slot in slots:

            slot_ocupado = None

            for consulta in consultas:
                if (consulta['data'] == data and consulta['horário'] == slot and consulta['especialidade'].upper() == especialidade.upper()):
                    slot_ocupado = consulta['id_médico']
            
            if slot_ocupado:

                info_med = next((med for med in med_especialistas if med['id'] == slot_ocupado), None)
                nome_md = info_med['nome']
                agenda[(dia_index,slot)] = {'médico': nome_md, 'marcada': True, 'id_médico': slot_ocupado}
            
            else:

                escolhido = random.choice(med_especialistas)
                agenda[(dia_index,slot)] = {'médico': escolhido['nome'], 'marcada': False, 'id_médico': escolhido['id']}
    
    return semana, slots, agenda

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

def main():

    view.run_interface()

if __name__ == "__main__":
    main()
