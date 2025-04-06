# CONTROLLER -> Controlo do Sistema, Funções de Arranque
import json
import projeto_model as model
import projeto_view as view
from datetime import datetime

def processo_registo(values):

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

def check_login(values):

    try:
        login = model.log_in(CC = int(values['-UTENTE_CC-']))

        if login:
            return True
        else:
            return False
        
    except:
        pass

def main():

    view.run_interface()

if __name__ == "__main__":
    main()