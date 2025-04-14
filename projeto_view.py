# VIEW -> Interface Gráfica
import PySimpleGUI as sg
import projeto_controller as control
import projeto_model as model
from datetime import date, timedelta, datetime

sg.theme_background_color("#FFC0E1") 
sg.theme_button_color(("white", "#FF69B4"))

def Layout_Inicial():

    menu_botões = [

        [sg.Button('Portal do Utente', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-UTENTE-'),
        sg.Button('Novo Registo de Utente', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-NOVO_REG-')],

        [sg.Button('Médicos Especialistas', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-MD-'),sg.Button('Campanha de Vacinação', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-VAC-')]
    ]

    layout = [[sg.Column(menu_botões, element_justification= 'center')]]

    return layout

def Novo_Reg_Layout():

    layout = [

        [sg.Text('Nome Completo *:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_NOME-'), sg.Input(key= '-NOME-')],
        [sg.Text('Data de Nascimento (A-M-D) *:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_DOB-'), sg.Input(key= '-DOB-')],
        [sg.Text('Sexo *:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_SEXO-'), sg.Combo(['M', 'F'], key= '-SEXO-')],
        [sg.Text('Condições Prévias:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_COND-'), sg.Input(key= '-COND-')],
        [sg.Text('Medicações (Nome: Dosagem):', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_MEDS-'), sg.Input(key= '-MEDS-')],
        [sg.Text('Número de Cartão de Cidadão *:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_CC-'), sg.Input(key= '-CC-')],
        [sg.Text('NIF *:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_NIF-'), sg.Input(key= '-NIF-')],
        [sg.Text('Localidade *:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_LOCAL-'), sg.Input(key= '-LOCAL-')],
        [sg.Text('Contacto Pessoal *:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_CP-'), sg.Input(key= '-CP-')],
        [sg.Text('Parente mais Próximo:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_NOK-'), sg.Input(key= '-NOK-')],
        [sg.Text('Contacto do Parente mais Próximo:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-REG_CNOK-'), sg.Input(key= '-CNOK-')],
        [sg.Button('Registar', font= ("Arial Rounded Mt Bold", 12), key= '-REGISTAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 12), key= '-CANCELAR-')]
    ]

    window = sg.Window('Novo Registo de Utente', layout, modal= True) # Utilizamos uma janela modal de modo a que não seja possível a interação com a janela principal durante o processo de registo!

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-REGISTAR-':

            if (not values['-NOME-'] or not values['-DOB-'] or not values['-SEXO-'] or not values['-NIF-'] or not values['-CP-'] or not values['-LOCAL-']):
                sg.popup('Por favor preencha os campos obrigatórios (*)!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
                continue

            # Verificação do Formato de Input das Medicações
            input_med = values['-MEDS-'].strip()

            info_válida = False

            if input_med:
                meds = [med.strip() for med in input_med.split(',') if med.strip()]

                # A utilização da função all() irá retornar True se o formato de input for correto!!
                info_válida = all((':' in med and len(med.split(':')) == 2 and med.split(':')[0].strip() and med.split(':')[1].strip()) for med in meds)
                
            else: info_válida = True # O campo de histórico de medicações não é obrigatório, por isso, não há problema se não for preenchido

            if not info_válida:
                sg.popup('Por favor introduza as suas medicações no formato pedido (Nome: Dosagem)!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
                continue

            res = control.processar_registo(values)
            sg.popup(res, font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')

def Log_In_Layout():

    layout = [

        [sg.Text('Número de Cartão de Cidadão:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-LOG_CC-'), sg.Input(key= '-UTENTE_CC-')],
        [sg.Button('Entrar', font= ("Arial Rounded Mt Bold", 12), key= '-ENTRAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 12), key= '-CANCELAR-')]
    ]

    window = sg.Window('Log In de Utente', layout, modal= True) # Utilizamos uma janela modal de modo a que não seja possível a interação com a janela principal!

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-ENTRAR-':

            res = control.check_login(values)

            if res is True:

                window.close()
                Portal_Utente_Layout()

            elif res is False:
                sg.popup('Registo de utente não encontrado! Por favor, realize a sua inscrição na plataforma.', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')

def Portal_Utente_Layout():

    paciente = control.info_paciente_logged()
    paciente_id = paciente.get('id')

    up =  '▶'
    down =  '▼'

    certificados = [ # Lista de certificados de vacinação

    ]

    hist_consultas = [ # Tabela com consultas (dia, médico, especialidade)

    ]

    hist_medicações = [ # Tabela com medicações (nome da prescrição, dosagem)

    ]

    def abrir(layout, key):
        return sg.pin(sg.Column(layout,key= key, visible= False)) # O método sg.pin permite aceder ao display de cada coluna!

    layout = [
        
        [sg.Text(up, enable_events= True, key= '-ABRE_CONS-', text_color= 'white', background_color= '#FF69B4') ,sg.Text('Histórico de Consultas', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-HIST_CONS-')],
        [abrir(hist_consultas, 'CONS')],
        [sg.Text(up, enable_events= True, key= '-ABRE_PRESC-', text_color= 'white', background_color= '#FF69B4') ,sg.Text('Histórico de Prescrições Médicas', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-HIST_PRESC-')],
        [abrir(hist_medicações, 'PRESC')],
        [sg.Text(up, enable_events= True, key= '-ABRE_CERTIF-', text_color= 'white', background_color= '#FF69B4') ,sg.Text('Certificados de Vacinação', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-CERTIF-')],
        [abrir(certificados, 'CERTIF')],
        [sg.Button('Marcar Consulta', font= ("Arial Rounded Mt Bold", 12), key= '-MARCAR-'), sg.Button('Sair', font= ("Arial Rounded Mt Bold", 12), key= '-SAIR-')]
    ]

    window = sg.Window('Portal do Utente', layout, size=(300,140))

    aberto_cons = False
    aberto_presc = False
    aberto_certif = False

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return
        
        elif event == '-ABRE_CONS-':

            aberto_cons = not aberto_cons
            window['-ABRE_CONS-'].update(down if aberto_cons else up)
            window['CONS'].update(visible= aberto_cons)

        elif event == '-ABRE_PRESC-':

            aberto_presc = not aberto_presc
            window['-ABRE_PRESC-'].update(down if aberto_presc else up)
            window['PRESC'].update(visible= aberto_presc)

        elif event == '-ABRE_CERTIF-':

            aberto_certif = not aberto_certif
            window['-ABRE_CERTIF-'].update(down if aberto_certif else up)
            window['CERTIF'].update(visible= aberto_certif)

        elif event == '-MARCAR-':

            especialidade = Especialidade_Cons_Layout()
            if especialidade:
                Agenda_Cons_Layout(especialidade, paciente_id)

def Especialidade_Cons_Layout():
    
    especialidades = [med['especialidade'] for med in model.médicos]

    layout = [

        [sg.Text('Especialidade da Consulta:', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4'), sg.Combo(especialidades, key= '-SEL_ESPEC-', readonly= True)],
        [sg.Text('CARDIOlogia, PNEUMologia, CLÍNICA Geral, ORTOpedia, OB/GIN, Medicina DENTária, PEDIATria', font= ("Arial Rounded Mt Bold", 10), text_color= 'white', background_color= '#FF69B4', key= '-CÓDIGO-')],
        [sg.Button('Avançar', font= ("Arial Rounded Mt Bold", 12), key= '-AVANÇAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 12), key= '-CANCELAR-')]
    ]

    window = sg.Window('Seleção de Especialidade', layout, modal= True)
    
    while True:
    
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-AVANÇAR-':

            if values.get('-SEL_ESPEC-'):

                window.close()
                return values['-SEL_ESPEC-']
            else:
                sg.popup('Por favor selecione uma especialidade para avançar!')

def Agenda_Cons_Layout(especialidade, paciente_id):

    # Construção de slots para a semana atual
    hoje = date.today()
    início_semana = hoje - timedelta(days= hoje.weekday()) # Segunda-feira da semana atual
    semana, slots, agenda = control.agenda_especialidade(especialidade, início_semana)


    # Cabeçalhos da tabela -> Dias da Semana (Segunda - Sábado)
    header = [sg.Text('Horário', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', size= (12,1), pad= (1,1))]
    for i, dia in enumerate(semana):
        header.append(sg.Text(dia.strftime("%a %d/%m"), key= ('-HEADER-', i), size= (13,1), font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', justification= 'center', pad= (1,1)))

    # Linhas da tabela -> Slots de Tempo (intervalos de 30 minutos)
    colunas = []
    for slot in slots:

        coluna = [sg.Text(slot, font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', size= (12,1), pad= (1,1))]

        for dia_index in range(len(semana)):

            info = agenda.get((dia_index, slot))
            if info:

                bg_color = 'green' if not info['marcada'] else 'red' # Slots disponíveis -> VERDE, Slots ocupados -> VERMELHO
                coluna.append(sg.Button(info['médico'], key= ('-SLOT-', dia_index, slot, info['id_médico']), size= (12,1), font= ("Arial Rounded Mt Bold", 14), button_color= ('white', bg_color), pad= (1,1)))
            else:
                coluna.append(sg.Text('--', size= (12,1), font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', pad= (1,1)))
        colunas.append(coluna)
    
    # Navegação entre semanas (Semana Anterior, Semana Seguinte)
    layout = [header] + colunas + [

        [sg.Button('Semana Anterior', font= ("Arial Rounded Mt Bold", 12), key= '-ANTERIOR-', pad=(5, 5)), 
        sg.Button('Semana Seguinte', font= ("Arial Rounded Mt Bold", 12), key= '-SEGUINTE-', pad=(5, 5)), 
        sg.Button('Sair', font= ("Arial Rounded Mt Bold", 12), key= '-SAIR-', pad=(5, 5))]
    ]

    window = sg.Window('Agendamento de Consultas', layout, finalize= True)

    início_semana_atual = início_semana

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return
        
        elif event == '-SEGUINTE-': # Construção da tabela para a semana seguinte

            início_semana_atual = início_semana_atual + timedelta(days= 7) # Avançamos uma semana no calendário
            semana, slots, agenda = control.agenda_especialidade(especialidade, início_semana_atual)

            for i, dia in enumerate(semana):
                window[('-HEADER-', i)].update(dia.strftime('%a %d/%m'))
            
            for slot in slots:
                for dia_index in range(len(semana)):

                    info = agenda.get((dia_index, slot))
                    if info:

                        bg_color = 'green' if not info['marcada'] else 'red'
                        window[('-SLOT-', dia_index, slot, info['id_médico'])].update(text = info['médico'], button_color= ('white', bg_color))

        elif event == '-ANTERIOR-': # Construção da tabela para a semana anterior

            início_semana_atual = início_semana_atual - timedelta(days= 7) # Avançamos uma semana no calendário
            semana, slots, agenda = control.agenda_especialidade(especialidade, início_semana_atual)

            for i, dia in enumerate(semana):
                window[('-HEADER-', i)].update(dia.strftime('%a %d/%m'))
            
            for slot in slots:
                for dia_index in range(len(semana)):

                    info = agenda.get((dia_index, slot))
                    if info:

                        bg_color = 'green' if not info['marcada'] else 'red'
                        window[('-SLOT-', dia_index, slot, info['id_médico'])].update(text = info['médico'], button_color= ('white', bg_color))

        elif isinstance(event, tuple) and event[0] == '-SLOT-': # Marcação da consulta num slot disponível

            dia_index, slot, med_id = event[1], event[2], event[3]
            info = agenda.get((dia_index, slot))

            if info and not info['marcada']:

                data = semana[dia_index].strftime('%Y-%m-%d')
                Marcação_Cons_Layout(data, slot, info['médico'], med_id, especialidade, paciente_id)

                semana, slots, agenda = control.agenda_especialidade(especialidade, início_semana_atual)
                for i, dia in enumerate(semana):
                    window[('-HEADER-', i)].update(dia.strftime('%a %d/%m'))

                for slot in slots:
                    for dia_index in range(len(semana)):

                        info = agenda.get((dia_index, slot))
                        if info:

                            bg_color = 'green' if not info['marcada'] else 'red'
                            window[('-SLOT-', dia_index, slot, info['id_médico'])].update(text = info['médico'], button_color= ('white', bg_color))

def Marcação_Cons_Layout(data, slot, med_nome, med_id, especialidade, paciente_id):

    layout = [

        [sg.Text(f'Agendar consulta para o dia {data}, {slot}?', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4')],
        [sg.Text(f'Médico Especialista: {med_nome}', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4')],
        [sg.Button('Confirmar', font= ("Arial Rounded Mt Bold", 12), key= '-CONFIRMAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 12), key= '-CANCELAR-')]
    ]
    
    window = sg.Window('Confirmação de Agendamento', layout, modal=True)

    while True:
    
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-CONFIRMAR-':

            res = control.processar_marcar_consulta(data, slot, especialidade, med_id, paciente_id)
            sg.popup(res, font=("Arial Rounded Mt Bold", 14), text_color='white', background_color='#FFC0E1')
            window.close()

def Médicos_Esp_Layout():
    pass

def Campanha_Vac_Layout():
    pass

def run_interface():

    stop = False

    # JANELA PRINCIPAL
    window = sg.Window("Gestão de Saúde Comunitária", Layout_Inicial(), size=(560, 200), element_justification="center", finalize=True)

    while not stop:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            stop = True
        
        # Novo Registo de Pacientes
        elif event == '-NOVO_REG-':
            Novo_Reg_Layout()
        
        # Verificação de Log In de Pacientes -> Página Portal do Utente -> Marcação de Consultas
        elif event == '-UTENTE-':
            Log_In_Layout()
        
        # Informações sobre Médicos Especialistas
        elif event == '-MD-':
            Médicos_Esp_Layout()
        
        # Informação sobre Campanha de Vacinação
        elif event == '-VAC-':
            Campanha_Vac_Layout()

    window.close()
